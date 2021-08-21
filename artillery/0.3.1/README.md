# Artillery Service

Keptn service for [artillery.io](https://artillery.io/) load testing tool.

### Deploy in your Kubernetes cluster

To deploy the current version of the *artillery-service* in your Keptn Kubernetes cluster, apply the [`deploy/service.yaml`](deploy/service.yaml) file:

```console
kubectl apply -f deploy/service.yaml
```

This should install the `artillery-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment artillery-service -o wide
kubectl -n keptn get pods -l run=artillery-service
```

### Up- or Downgrading

Adapt and use the following command in case you want to up- or downgrade your installed version (specified by the `$VERSION` placeholder):

```console
kubectl -n keptn set image deployment/artillery-service artillery-service=keptnsandbox/artillery-service:$VERSION --record
```

### Uninstall

To delete a deployed *artillery-service*, use the file `deploy/*.yaml` files from this repository and delete the Kubernetes resources:

```console
kubectl delete -f deploy/service.yaml
```


## Usage

After deploying the `artillery-service` to your Keptn cluster, you can configure your test strategies by adding an `artillery.conf.yaml` file, allowing for more complex configurations like multiple test files for different stages.

```
---
spec_version: '0.1.0'
workloads:
  - teststrategy: functional
    script: scenarios/basic.yaml
  - teststrategy: performance_light
    script: scenarios/load.yaml
  - teststrategy: functional-light
    script: scenarios/health.yaml
```

The configuration file can be added to the repo using the `keptn add-resource` command:

```
keptn add-resource --project=PROJECTNAME --service=SERVICENAME --all-stages --resource=artillery.conf.yaml --resourceUri=scenarios/artillery.conf.yaml
```

If no `artillery.conf.yaml` file is provided the service will try to execute the default scenario `scenarios/load.yaml`. You can add and update the scenarios and add them to Keptn using:

```console
keptn add-resource --project=PROJECTNAME --service=SERVICENAME --stage=STAGENAME --resource=./scenarios/basic.yaml --resourceUri=scenarios/basic.yaml
```