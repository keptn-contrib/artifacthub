# OneChart Service

This is a Keptn Service that provides a default Helm Chart template that can be used to deploy a service.

The default Helm chart is [OneChart](https://gimlet.io/onechart/getting-started/) from the Gimlet project.

## Installation

### Deploy in your Kubernetes cluster

To deploy the current version of the *onechart-service* in your Keptn Kubernetes cluster, apply the [`deploy/service.yaml`](deploy/service.yaml) file:

```console
kubectl apply -f deploy/service.yaml
```

This should install the `onechart-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment onechart-service
kubectl -n keptn get pods -l run=onechart-service
```

### Uninstall

To delete a deployed *onechart-service*, use the file `deploy/*.yaml` files from this repository and delete the Kubernetes resources:

```console
kubectl delete -f deploy/service.yaml
```