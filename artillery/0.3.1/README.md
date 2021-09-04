# Keptn Artillery Service

Keptn service for [artillery.io](https://artillery.io/) load testing tool.

## Compatibility Matrix

| Keptn Version    | [artillery-service Docker Image](https://hub.docker.com/r/keptnsandbox/artillery-service/tags) | Comment |
:----------------:|:----------------------------------------:|:----------------:|
|       0.8.1      | keptnsandbox/artillery-service:0.1.0 | initial release |
|       0.8.2      | keptnsandbox/artillery-service:0.2.0 | |
|       0.8.3      | keptnsandbox/artillery-service:0.3.0 | |
|       0.8.4-0.8.5     | keptnsandbox/artillery-service:0.3.1 | |

## Installation

The *artillery-service* can be installed as a part of [Keptn's uniform](https://keptn.sh).

### Deploy in your Kubernetes cluster

To deploy the current version of the *artillery-service* in your Keptn Kubernetes cluster, apply the [`deploy/service.yaml`](https://github.com/keptn-sandbox/artillery-service/blob/master/deploy/service.yaml) file:

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

## Development

### Where to start

If you don't care about the details, your first entrypoint is [eventhandlers.go](https://github.com/keptn-sandbox/artillery-service/blob/master/eventhandlers.go). Within this file 
 you can add implementation for pre-defined Keptn Cloud events.
 
To better understand Keptn CloudEvents, please look at the [Keptn Spec](https://github.com/keptn/spec).
 
If you want to get more insights, please look into [main.go](https://github.com/keptn-sandbox/artillery-service/blob/master/main.go), [deploy/service.yaml](https://github.com/keptn-sandbox/artillery-service/blob/master/deploy/service.yaml),
 consult the [Keptn docs](https://keptn.sh/docs/) as well as existing [Keptn Core](https://github.com/keptn/keptn) and
 [Keptn Contrib](https://github.com/keptn-contrib/) services.

### Build yourself

* Build the binary: `go build -ldflags '-linkmode=external' -v -o artillery-service`
* Run tests: `go test -race -v ./...`
* Deploy the service using `kubectl`: `kubectl apply -f deploy/`
* Delete/undeploy the service using `kubectl`: `kubectl delete -f deploy/`
* Watch the deployment using `kubectl`: `kubectl -n keptn get deployment artillery-service -o wide`
* Get logs using `kubectl`: `kubectl -n keptn logs deployment/artillery-service -f`
* Watch the deployed pods using `kubectl`: `kubectl -n keptn get pods -l run=artillery-service`
* Deploy the service using [Skaffold](https://skaffold.dev/): `skaffold run --default-repo=your-docker-registry --tail` (Note: Replace `your-docker-registry` with your DockerHub username; also make sure to adapt the image name in [skaffold.yaml](skaffold.yaml))


### Testing Cloud Events

We have dummy cloud-events in the form of [RFC 2616](https://ietf.org/rfc/rfc2616.txt) requests in the [test-events/](test-events/) directory. These can be easily executed using third party plugins such as the [Huachao Mao REST Client in VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).