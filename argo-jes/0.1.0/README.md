# Argo Job-Executor Integration

This integration shows you how to run the [Argo-Service](https://github.com/keptn-contrib/argo-service) as a Kubernetes job using the [Job-executor-service](https://github.com/keptn-contrib/job-executor-service), reducing resource usage on the cluster and making the configuration a lot easier.

## Installation

Please follow the [Job-Executor documentation](https://github.com/keptn-contrib/job-executor-service) for the installation process.

## Configure Argo using the Job-Executor

## Step 1: Create Kubernetes Service-Account

To execute Argo rollouts functionality the Kubernetes pod needs specific permissions that the Job-Executor-Service blocks by default. The following `ServiceAccount` provides the required permissions and can be used inside the `job.config.yaml` using the `serviceAccount` parameter.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: "jes-argo"
  namespace: keptn-jes
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: keptn-argo-service-rollouts
  labels:
    "app": "keptn"
rules:
  - apiGroups:
      - "argoproj.io"
    resources:
      - rollouts
    verbs:
      - "*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: keptn-argo-rollouts
  labels:
    app.kubernetes.io/component: rollouts-controller
    app.kubernetes.io/name: argo-rollouts-clusterrole
    app.kubernetes.io/part-of: argo-rollouts
rules:
  - apiGroups:
      - argoproj.io
    resources:
      - rollouts
      - rollouts/status
      - rollouts/finalizers
    verbs:
      - get
      - list
      - watch
      - update
      - patch
  - apiGroups:
      - argoproj.io
    resources:
      - analysisruns
      - analysisruns/finalizers
      - experiments
      - experiments/finalizers
    verbs:
      - create
      - get
      - list
      - watch
      - update
      - patch
      - delete
  - apiGroups:
      - argoproj.io
    resources:
      - analysistemplates
      - clusteranalysistemplates
    verbs:
      - get
      - list
      - watch
  # replicaset access needed for managing ReplicaSets
  - apiGroups:
      - apps
    resources:
      - replicasets
    verbs:
      - create
      - get
      - list
      - watch
      - update
      - patch
      - delete
  # services patch needed to update selector of canary/stable/active/preview services
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - get
      - list
      - watch
      - patch
  # secret read access to run analysis templates which reference secrets
  - apiGroups:
      - ""
    resources:
      - secrets
    verbs:
      - get
      - list
      - watch
  # pod list/update needed for updating ephemeral data
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - list
      - update
      - watch
  # pods eviction needed for restart
  - apiGroups:
      - ""
    resources:
      - pods/eviction
    verbs:
      - create
  # event write needed for emitting events
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - update
      - patch
  # ingress patch needed for managing ingress annotations, create needed for nginx canary
  - apiGroups:
      - networking.k8s.io
      - extensions
    resources:
      - ingresses
    verbs:
      - create
      - get
      - list
      - watch
      - patch
  # job access needed for analysis template job metrics
  - apiGroups:
      - batch
    resources:
      - jobs
    verbs:
      - create
      - get
      - list
      - watch
      - update
      - patch
      - delete
  # virtualservice access needed for using the Istio provider
  - apiGroups:
      - networking.istio.io
    resources:
      - virtualservices
    verbs:
      - watch
      - get
      - update
      - list
  # trafficsplit access needed for using the SMI provider
  - apiGroups:
      - split.smi-spec.io
    resources:
      - trafficsplits
    verbs:
      - create
      - watch
      - get
      - update
      - patch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: keptn-argo-service-rollouts
  labels:
    "app": "keptn"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: keptn-argo-rollouts
#  name: keptn-argo-service-rollouts
subjects:
  - kind: ServiceAccount
    name: "jes-argo"
    namespace: keptn-jes
```

Add the service account to your Kubernetes cluster:

```bash
kubectl apply -f serviceaccount.yaml
```

### Step 2: Add the Job-Executor configuration file

The following configuration will allow you to run `argo rollouts promote` and `argo rollouts abort` using the Job-Executor-Service whenever the correct Keptn event is triggered.

```yaml
apiVersion: v2
actions:
  - name: "Run Argo promote"
    events:
      - name: "sh.keptn.event.release.triggered"
        jsonpath:
          property: "$.data.deployment.deploymentstrategy"
          match: "user_managed"
    tasks:
      - name: "Execute Argo promote"
        image: "quay.io/argoproj/kubectl-argo-rollouts"
        args: ["promote", "$(SERVICE)-$(STAGE)", "-n", "$(PROJECT)-$(STAGE)"]
        serviceAccount: "jes-argo"
        env:
          - name: SERVICE
            value: "$.data.service"
            valueFrom: event
          - name: STAGE
            value: "$.data.stage"
            valueFrom: event
          - name: PROJECT
            value: "$.data.project"
            valueFrom: event

  - name: "Run Argo rollback"
    events:
      - name: "sh.keptn.event.rollback.triggered"
    tasks:
      - name: "Execute argo rollback"
        image: "quay.io/argoproj/kubectl-argo-rollouts"
        args: [ "abort", "$(SERVICE)-$(STAGE)", "-n", "$(PROJECT)-$(STAGE)" ]
        serviceAccount: "jes-argo"
        env:
          - name: SERVICE
            value: "$.data.service"
            valueFrom: event
          - name: STAGE
            value: "$.data.stage"
            valueFrom: event
          - name: PROJECT
            value: "$.data.project"
            valueFrom: event

  - name: "Argo test canary"
    events:
      - name: "sh.keptn.event.test.triggered"
        jsonpath:
          property: "$.data.test.teststrategy"
          match: "real-user"
    tasks:
      - name: "Wait for canary wait duration"
        image: "alpine"
        cmd: [ "sleep" ]
        args: [ "60s" ]
```

Add the job-executor configuration file to your Keptn service:

```bash
keptn add-resource --project=pod-tato-head --stage=production --service=helloservice --resource=job.config.yaml --resourceUri=job/config.yaml
```

Now the Job-Executor service will execute the Argo rollouts whenever you trigger a new evaluation.

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
