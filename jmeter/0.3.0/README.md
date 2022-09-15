# JMeter Job-Executor Integration

This integration shows you how to leverage [Job-executor-service](https://github.com/keptn-contrib/job-executor-service) for running load tests using `JMeter` on your Kubernetes cluster.

**Please note, that the instructions provided here enable you to run and configure your Kubernetes deployments using the job-executor-service. They are in no way intended to be a complete reference of Kubernetes, nor JMeter, nor Keptn.**

## Installation and Configuration

### Step 1: Install the Job-Executor in your cluster

Install [Job-Executor](https://github.com/keptn-contrib/job-executor-service) in a version compatible with your Keptn installation (see [GitHub Releases page](https://github.com/keptn-contrib/job-executor-service/releases), e.g., version 0.2.5 is compatible with Keptn 0.17.x), and make sure it is subscribed to the following Keptn Cloud Events:

* `sh.keptn.event.test.triggered`

This can verified in Keptn Bridge -> Project -> Settings -> Integrations -> job-executor-service.

**Example Installation Instructions**
 Please update `JES_VERSION` and `JES_NAMESPACE` in the example below according to your needs.

```bash
TASK_SUBSCRIPTION='sh.keptn.event.test.triggered'
JES_VERSION=0.2.5
JES_NAMESPACE=keptn-jes

helm upgrade --install --create-namespace -n ${JES_NAMESPACE} \
  job-executor-service https://github.com/keptn-contrib/job-executor-service/releases/download/${JES_VERSION}/job-executor-service-${JES_VERSION}.tgz \
  --set remoteControlPlane.autoDetect.enabled="true",remoteControlPlane.topicSubscription="${TASK_SUBSCRIPTION}",remoteControlPlane.api.token="",remoteControlPlane.api.hostname="",remoteControlPlane.api.protocol=""
 ```

**If you have installed jmeter-service, uninstall it**

```bash
helm uninstall jmeter-service -n keptn
```

### Step 2: Build your own JMeter Docker image

Since there are no official JMeter Docker images, we recommend to build your own (and customize it). Here is a Dockerfile with a basic JMeter installation, feel free to adapt!

```docker
FROM alpine:3.15
ENV env=production
ARG JMETER_VERSION="5.4.3"
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

# Uncomment lines below for debug output
# echo "Test.log"
# cat /keptn/jmeter/test.log

# echo "log.tlf"
# cat /keptn/jmeter/log.tlf
```

Now you will need to build the Docker image and push it to your image registry, e.g., `docker.io/yourorg/jmeter:latest`.

```bash
docker build -t docker.io/yourorg/jmeter:latest .
docker push docker.io/yourorg/jmeter:latest
```

### Step 3: Make sure your project is set up properly with the right tasks.

While technically not part of the installation instructions, it is worthwhile to mention the coupling between Keptn's shipyard file, and the respective Cloud Event Types configured for Job Executor. 

In example, you should have a monitoring provider (e.g,. Prometheus) configured already for `evaluation` tasks. In addition, your shipyard should contain at least one stages with a `delivery` sequence. Last but not least, the example below also contains a `deployment` step. You can skip this, and just adapt the `JSERVER_URL` in the job-executor config below.

Example:
```yaml
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "shipyard-delivery"
spec:
  stages:
    - name: "qa"
      sequences:
        - name: "delivery"
          tasks:
            - name: "deployment"
            - name: "test"
              properties:
                teststrategy: performance
```

### Step 4: Add the Job-Executor configuration file

The following Job Executor configuration (referred to as job config or `job/config.yaml`) allows you to run jmeter with the `load.jmx` file (e.g., from the [Keptn Carts example](https://github.com/keptn/examples/tree/master/onboarding-carts/jmeter)) using whenever a `test.triggered` with `teststrategy=performance` event is sent by Keptn.

Add the following content to a file called *jmeter-job-config.yaml* in your current working directory:
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
          - '-JSERVER_URL=$(KEPTN_SERVICE).$(KEPTN_PROJECT)-$(KEPTN_STAGE).svc.cluster.local'
          - '-j'
          - '/keptn/jmeter/test.log'
          - '-l'
          - '/keptn/jmeter/log.tlf'
```

Add the job-executor configuration file to your Keptn service and stage:

```bash
PROJECT=sockshop
SERVICE=carts

keptn add-resource --project=$PROJECT --service=$SERVICE --stage=staging --resource=jmeter-job-config.yaml --resourceUri=job/config.yaml
```

## Run it

Now the Job-Executor-Service will execute the JMeter tests whenever you trigger a delivery, e.g., 
```bash
IMAGE="docker.io/keptnexamples/carts"
VERSION=0.13.1

keptn trigger delivery --project=$PROJECT --service=$SERVICE --stage=staging --image=$IMAGE:$VERSION --labels=version=$VERSION
```

Eventually you should see the `deployment` and `test` events in Keptn Bridge:

![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/jmeter/0.3.0/images/keptn-bridge.png)


## Limitations

Currently, there are a few open problems when using jmeter via Job Executor Service:

- JMeter CLI does not throw an error when the tests fail but instead just returns the results. These results cannot be evaluated directly in JMeter.
- Tests towards a non-existing or non-reachable endpoint take a very long time (15+ min) and currently don't have a timeout. 

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
