# JMeter Job-Executor Integration

This integration shows you how to run JMeter as a Kubernetes job using the [Job-executor-service](https://github.com/keptn-contrib/job-executor-service), reducing resource usage on the cluster since JMeter will only run if a test is triggered.

**Note: This integration still has some restrictions! See the [restrictions section](#restrictions) for more information.**

## Prerequisites 

### Step 1: Install the Job-Executor in your cluster

Please follow the [Job-Executor documentation](https://github.com/keptn-contrib/job-executor-service) for the installation process.

### Step 2: Disable the JMeter-Service

Disable normal jmeter-service (in case you don't want to run it in parallel):

```
kubectl scale deployment/jmeter-service -n "keptn" --replicas=0
```

### Step 3: Build your own JMeter Docker image

Since JMeter has no official Docker image you will have to build your own one. Here is a Dockerfile with a basic JMeter installation.

```docker
FROM alpine:3.13
ENV env=production
ARG JMETER_VERSION="5.1.1"
ENV JMETER_HOME /opt/apache-jmeter-${JMETER_VERSION}
ENV	JMETER_BIN	${JMETER_HOME}/bin
ENV	JMETER_DOWNLOAD_URL  https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz

# Load additional extensions
ARG DYNATRACE_EXTENSION_VERSION="1.3"
ENV DYNATRACE_EXTENSION_URL https://github.com/dynatrace-oss/jmeter-dynatrace-plugin/releases/download/v${DYNATRACE_EXTENSION_VERSION}.snapshot/jmeter-dynatrace-plugin-${DYNATRACE_EXTENSION_VERSION}-SNAPSHOT.jar

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
	&& rm -rf /var/cache/apk/* \
	&& mkdir -p /tmp/dependencies  \
	&& curl -L --silent ${JMETER_DOWNLOAD_URL} >  /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz  \
	&& mkdir -p /opt  \
	&& tar -xzf /tmp/dependencies/apache-jmeter-${JMETER_VERSION}.tgz -C /opt  \
	&& rm -rf /tmp/dependencies \
	&& curl -L --silent ${DYNATRACE_EXTENSION_URL} > /opt/apache-jmeter-${JMETER_VERSION}/lib/ext/jmeter-dynatrace-plugin-${DYNATRACE_EXTENSION_VERSION}-SNAPSHOT.jar

# Set global PATH such that "jmeter" command is found
ENV PATH $PATH:$JMETER_BIN

# Entrypoint has same signature as "jmeter" command
COPY entrypoint.sh /

WORKDIR	/keptn/jmeter

ENTRYPOINT ["/entrypoint.sh"]
```

The entrypoint file executes JMeter using the passed arguments. You can also uncomment the commands below to enable some debugging steps.

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

## Configure JMeter using the Job-Executor

### Step 1: Add the Job-Executor configuration file

The following configuration will allow you to run the `basiccheck.jmx` on the Keptn Sockshop project using the Job-Executor-Service whenever a test event is triggered.

```bash
apiVersion: v2
actions:
  - name: "Run JMeter"
   events:
    - name: "sh.keptn.event.test.triggered"
     jsonpath:
      property: "$.data.test.teststrategy"
      match: "functional"
    - name: "sh.keptn.event.test.triggered"
     jsonpath:
      property: "$.data.test.teststrategy"
      match: "performance"
   tasks:
    - name: "Run jmeter smoke tests"
     files:
      - jmeter/basiccheck.jmx
      - jmeter/load.jmx
     image: "gabrieltanner/jmeter:latest"
     args:
     - '-n'
     - '-t'
     - '/keptn/jmeter/basiccheck.jmx'
     - '-JPROTOCOL=http'
     - '-JSERVER_PROTOCOL=http'
     - '-JVUCount=10'
     - '-JLoopCount=10'
     - '-JSERVER_URL=ENDPOINT'
     - '-j'
     - '/keptn/jmeter/test.log'
     - '-l'
     - '/keptn/jmeter/log.tlf'
     env:
      - name: HOST
       value: "$.data.deployment.deploymentURIsLocal[0]"
       valueFrom: event
      - name: DEPLOYMENT
       value: "$.data.deployment"
       valueFrom: event
```

The following command can be used to add the configuration file to your Keptn service:

```bash
keptn add-resource --project=sockshop --service=carts --stage=staging --resource=jmeter.yaml --resourceUri=job/config.yaml
```

Now the Job-Executor service will execute the JMeter tests whenever you trigger a new evaluation.

## Restrictions

Currently, there are a few problems with this approach that cannot be fixed/addressed using the Job-Executor-Service:

- JMeter does not throw an error when the tests fail but instead just returns the results. These results cannot be evaluated without some custom code which cannot be added with the current Job-Executor features.
- Tests on a non-existing endpoint take a very long time (15+ min) and currently don't have a timeout. Such a case triggers the `max poll count` defined by the Job which therefore fails. This could probably be addressed by adding a parameter to the JMeter command.
- There is no official JMeter image and the users would have to provide their own one.

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
