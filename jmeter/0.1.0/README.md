# JMeter Job-Executor Integration

This integration shows you how to run JMeter as a Kubernetes job using the [Job-executor-service](https://github.com/keptn-contrib/job-executor-service), reducing resource usage on the cluster since JMeter will only run if a test is triggered.

**Note: This integration still has some restrictions! See the [restrictions section](#restrictions) for more information.**

## Installation

### Step 1: Install the Job-Executor in your cluster

Please follow the [Job-Executor documentation](https://github.com/keptn-contrib/job-executor-service) for the installation process.

### Step 2: Disable the JMeter-Service

In case you have installed Keptns jmeter-service (e.g., `keptn install --use-case continuous-delivery` or `helm install jmeter-service https://github.com/keptn/keptn/releases/download/<KEPTN_VERSION>/jmeter-service-<KEPTN_VERSION>.tgz -n keptn --create-namespace --wait`), you can either temporarily disable or uninstall jmeter-service:

**Temporary disable keptn/jmeter-service:**

```bash
kubectl scale deployment/jmeter-service -n "keptn" --replicas=0
```

Use
```bash
kubectl scale deployment/jmeter-service -n "keptn" --replicas=1
```
to re-enable it.

**Uninstall keptn/jmeter-service:**

```bash
helm uninstall jmeter-service -n keptn
```


### Step 3: Build your own JMeter Docker image

Since there are no official JMeter Docker images, we recommend to build your own (and customize it). Here is a Dockerfile with a basic JMeter installation, feel free to adapt!

```docker
FROM alpine:3.15
ENV env=production
ARG JMETER_VERSION="5.4.2"
ENV JMETER_HOME /opt/apache-jmeter-${JMETER_VERSION}
ENV	JMETER_BIN	${JMETER_HOME}/bin
ENV	JMETER_DOWNLOAD_URL  https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz

# Install extra packages
# See https://github.com/gliderlabs/docker-alpine/issues/136#issuecomment-272703023
# Change TimeZone TODO: TZ still is not set!
ARG TZ="Europe/Amsterdam"
RUN    apk update \
	&& apk upgrade \
	&& apk add ca-certificates libc6-compat \
	&& update-ca-certificates \
	&& apk add --update openjdk8-jre tzdata curl unzip bash \
	&& apk add --no-cache nss \
	&& rm -rf /var/cache/apk/*

# install jmeter
RUN mkdir -p /tmp/dependencies  \
	&& curl -L --silent ${JMETER_DOWNLOAD_URL} >  /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz  \
	&& mkdir -p /opt  \
	&& tar -xzf /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz -C /opt  \
	&& rm -rf /tmp/dependencies

# Set global PATH such that "jmeter" command is found
ENV PATH $PATH:$JMETER_BIN

# Entrypoint has same signature as "jmeter" command
COPY entrypoint.sh /

WORKDIR	/keptn/jmeter

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

The `entrypoint.sh` file executes JMeter using the passed arguments. You can also uncomment the commands below to enable some debugging steps.

```bash
#!/bin/bash
echo "jmeter args=$@"

echo "START Running Jmeter on `date`"

jmeter $@

echo "END Running Jmeter on `date`"

# Debugging
# echo "Test.log"
# cat /keptn/jmeter/test.log

# echo "log.tlf"
# cat /keptn/jmeter/log.tlf
```

Now you will need to build the Docker image and push it to your image registry.

```bash
docker build -t yourorg/jmeter:latest .
docker push yourorg/jmeter:latest
```

## Configure JMeter using the Job-Executor

### Step 1: Add the Job-Executor configuration file

The following configuration will allow you to run the `basiccheck.jmx` (e.g., from the [Keptn Carts example](https://github.com/keptn/examples/tree/master/onboarding-carts/jmeter)) using the Job-Executor-Service whenever a test event is triggered.

```yaml
apiVersion: v2
actions:
  - name: "Run JMeter"
    events:
      - name: "sh.keptn.event.test.triggered"
        jsonpath:
          property: "$.data.test.teststrategy"
          match: "performance"
    tasks:
      - name: "Run jmeter smoke tests"
        files:
          - jmeter/load.jmx
        image: "docker.io/yourorg/jmeter:latest"
        args:
          - '-n'
          - '-t'
          - '/keptn/jmeter/load.jmx'
          - '-JPROTOCOL=http'
          - '-JSERVER_PROTOCOL=http'
          - '-JVUCount=10'
          - '-JLoopCount=10'
          - '-JSERVER_URL=$SERVICE.$PROJECT-$STAGE.svc.cluster.local'
          - '-j'
          - '/keptn/jmeter/test.log'
          - '-l'
          - '/keptn/jmeter/log.tlf'
        env:
          - name: SERVICE
            value: "$.data.service"
            valueFrom: event
          - name: PROJECT
            value: "$.data.project"
            valueFrom: event
          - name: STAGE
            value: "$.data.stage"
            valueFrom: event
```

Add the job-executor configuration file to your Keptn service:

```bash
keptn add-resource --project=sockshop --service=carts --stage=staging --resource=jmeter.yaml --resourceUri=job/config.yaml
```

Now the Job-Executor service will execute the JMeter tests whenever you trigger a new evaluation.

## Restrictions

Currently, there are a few open problems when using jmeter via Job Executor Service:

- JMeter CLI does not throw an error when the tests fail but instead just returns the results. These results cannot be evaluated without some custom code which cannot be added with the current Job-Executor features.
- Tests on a non-existing endpoint take a very long time (15+ min) and currently don't have a timeout. Such a case triggers the `max poll count` defined by the Job which therefore fails. This could probably be addressed by customizing JMeter CLI parameters.

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
