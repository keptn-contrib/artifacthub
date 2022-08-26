# Helm Job-Executor Integration

This integration shows you how to leverage [Job-executor-service](https://github.com/keptn-contrib/job-executor-service) for deployment with `helm` on your Kubernetes cluster.

**Please note, that the instructions provided here serve the purpose of enabling you to run and configure your Kubernetes deployments using job-executor-service. They are in no way intended to be a complete reference of Kubernetes, nor Helm, nor Keptn.**

## Installation and Configuration

### Step 1: Install the Job-Executor in your cluster

Install [Job-Executor documentation](https://github.com/keptn-contrib/job-executor-service), and make sure it is subscribed to the following Keptn Cloud Events:

* `sh.keptn.event.deployment.triggered` (for actual deployments)
* `sh.keptn.event.rollback.triggered` (for rollback sequence, i.e., when a previous deployment does not go well)
* `sh.keptn.event.action.triggered` (for remediation sequence)

**Example Installation Instruction for Job Executor**
```bash
TASK_SUBSCRIPTION='sh.keptn.event.deployment.triggered\,sh.keptn.event.rollback.triggered\,sh.keptn.event.action.triggered'
JES_VERSION=0.2.5-next.0
JES_NAMESPACE=keptn-jes

helm upgrade --install --create-namespace -n ${JES_NAMESPACE} \
  job-executor-service https://github.com/keptn-contrib/job-executor-service/releases/download/${JES_VERSION}/job-executor-service-${JES_VERSION}.tgz \
  --set remoteControlPlane.autoDetect.enabled="true",remoteControlPlane.topicSubscription="${TASK_SUBSCRIPTION}",remoteControlPlane.api.token="",remoteControlPlane.api.hostname="",remoteControlPlane.api.protocol=""
```

**In case you have installed helm-service, please uninstall it**
```bash
helm uninstall jmeter-service -n keptn
```

### Step 2: Make sure your project is setup properly with the right tasks

While technically not part of the installation instructions, it is worthwhile to mention the coupling between Keptn's shipyard file, and the respective Cloud Event Types configured for Job-Executor-Service. 

In example, you should have a monitoring provider (e.g,. Prometheus) configured already for `evaluation` tasks. In addition, for best results, your shipyard should contain at least one, better two stages, a `delivery` sequence, a `rollback` sequence, and a `remediation` sequence.

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
            - name: "evaluation"
              properties:
                timeframe: "2m"

        - name: "rollback"
          triggeredOn:
            - event: "qa.delivery.finished"
              selector:
                match:
                  result: "fail"
          tasks:
            - name: "rollback"

    - name: "production"
      sequences:
        - name: "delivery"
          triggeredOn:
            - event: "qa.delivery.finished"
          tasks:
            - name: "approval"
              properties:
                pass: "manual"
                warning: "manual"
            - name: "deployment"


        - name: "remediation"
          triggeredOn:
            - event: "production.remediation.finished"
              selector:
                match:
                  evaluation.result: "fail"
          tasks:
            - name: "get-action"
            - name: "action"
            - name: "evaluation"
              triggeredAfter: "2m"
              properties:
                timeframe: "2m"

```

### Step 3: Add the Job-Executor configuration file

The following job-executor configuration file (referred to as job config or `job/config.yaml`) allows you to
* deploy using `helm upgrade`,
* rollback using `helm rollback`, and
* scale up as a remediation action using `kubectl`

Add the following content to a file called *helm-job-config.yaml* in your current working directory:
```yaml
apiVersion: v2
actions:
  - name: "Deploy using helm"
    events:
      - name: "sh.keptn.event.deployment.triggered"
    tasks:
      - name: "Run helm"
        files:
          - /charts
        env:
          - name: IMAGE
            value: "$.data.configurationChange.values.image"
            valueFrom: event
        image: "alpine/helm:3.7.2"
        serviceAccount: "jes-deploy-using-helm"
        cmd: ["helm"]
        args: ["upgrade", "--create-namespace", "--install", "-n", "$(KEPTN_PROJECT)-$(KEPTN_STAGE)", "$(KEPTN_SERVICE)", "/keptn/charts/$(KEPTN_SERVICE).tgz", "--set", "image=$(IMAGE)", "--wait"]

  - name: "Rollback using helm"
    events:
      - name: "sh.keptn.event.rollback.triggered"
    tasks:
      - name: "Run helm"
        serviceAccount: "jes-deploy-using-helm"
        image: "alpine/helm:3.7.2"
        cmd: ["helm"]
        args: ["rollback", "-n", "$(KEPTN_PROJECT)-$(KEPTN_STAGE)", "$(KEPTN_SERVICE)", "--wait"]

  - name: "Scale using kubectl"
    events:
      - name: "sh.keptn.event.action.triggered"
        jsonpath:
          property: "$.data.action.action"
          match: "scaling"
    tasks:
      - name: "Run kubectl"
        serviceAccount: "jes-deploy-using-helm"
        env:
          - name: SCALING
            value: $.data.action.value
            valueFrom: event
        image: "alpine/k8s:1.20.15"
        cmd: ["sh"]
        # Note: Hardcoded kubernetes namespace & KEPTN_SERVICE does most likely not match the deployment name
        args: ["-c", "REPLICAS=$(kubectl -n ${KEPTN_PROJECT}-${KEPTN_STAGE} get deployment/${KEPTN_SERVICE} -o go-template='{{.spec.replicas}}');DESIRED=$((${SCALING}+${REPLICAS}));echo Scaling deployment to ${DESIRED} && kubectl -n ${KEPTN_PROJECT}-${KEPTN_STAGE} scale --replicas=${DESIRED} deployment/${KEPTN_SERVICE}"]
```

Add the job-executor configuration file to your Keptn service and stage:

```bash
PROJECT=podtato-head
SERVICE=helloservice

keptn add-resource --project=$PROJECT --service=$SERVICE --all-stages --resource=helm-job-config.yaml --resourceUri=job/config.yaml
```

**Accessing the Kubernetes API**

By default, job-executor-service does not grant access to the Kubernetes api, the respective jobs (e.g., `helm install` or `helm upgrade`) would fail with `The connection to the server localhost:8080 was refused - did you specify the right host or port?`.

The easiest (and also most insecure) way to have such a service account on Kubernetes is to apply the following Kubernetes manifest. 
Please create a file called *k8s-jes-deploy-using-helm.yaml* with the following content:
```yaml
apiVersion: v1
automountServiceAccountToken: true
kind: ServiceAccount
metadata:
  name: jes-deploy-using-helm
  namespace: keptn-jes
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: keptn-jes-deploy-using-helm
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: jes-deploy-using-helm
    namespace: keptn-jes
```

and apply it using

```bash
kubectl apply -f k8s-jes-deploy-using-helm.yaml
```

For more locked down setups, we recommend creating a dedicated Service Account and only link the needed roles/permissions depending on your Helm Chart. For more details, we recommend reading about [RBAC in the Kubernetes docs](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).

### Step 4: Add your services helm Chart

Last but not least, in order for the `helm` command and the respective job config to find your Helm Charts, they need to be put into the `charts/ folder in Keptn, e.g.:
```bash
PROJECT=podtato-head
SERVICE=helloservice

keptn add-resource --project=$PROJECT --service=$SERVICE --all-stages --resource=./helm/helloservice.tgz --resourceUri=charts/$SERVICE.tgz
```

## Test it

The way this example is provided, it should integrate nicely with the Keptn CLI as well as Keptn Bridge. In order to test it, you just need to trigger a delivery sequence, e.g.,
```bash
IMAGE="ghcr.io/podtato-head/podtatoserver"
VERSION=v0.1.1

keptn trigger delivery --project=$PROJECT --service=helloservice --image=$IMAGE:$VERSION --labels=version=$VERSION
```

To test the evaluation and rollback, you can try to deliver a slower version of podtato-head:
```bash
SLOW_VERSION=v0.1.2

keptn trigger delivery --project=$PROJECT --service=helloservice --image=$IMAGE:$SLOW_VERSION --labels=version=$SLOW_VERSION,slow=true
```

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
