# sumologic-service
![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-sandbox/sumologic-service)
[![Go Report Card](https://goreportcard.com/badge/github.com/keptn-sandbox/sumologic-service)](https://goreportcard.com/report/github.com/keptn-sandbox/sumologic-service)

This implements the `sumologic-service` that integrates the [Sumo Logic](https://en.wikipedia.org/wiki/Sumo_Logic) observability platform with Keptn. This enables you to use Sumo Logic as the source for the Service Level Indicators ([SLIs](https://keptn.sh/docs/0.15.x/reference/files/sli/)) that are used for Keptn [Quality Gates](https://keptn.sh/docs/concepts/quality_gates/).
If you want to learn more about Keptn visit us on [keptn.sh](https://keptn.sh)

Check the issue here for more info: https://github.com/keptn/integrations/issues/20


**BEFORE YOU START**, please be aware that there are more ways to integrate with your service that don't require creating a service from this template, see https://keptn.sh/docs/0.15.x/integrations/how_integrate/ for more details.

Examples:

* Webhooks: https://keptn.sh/docs/0.15.x/integrations/webhooks/
* Job-Executor-Service: https://github.com/keptn-sandbox/job-executor-service

## Quickstart
If you are on Mac or Linux, you can use [examples/kup.sh](https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/examples/kup.sh) to set up a local Keptn installation that uses Sumo Logic. This script creates a local minikube cluster, installs Keptn, Istio, Sumo Logic and the Sumo Logic integration for Keptn (check the script for pre-requisites). 

To use the script,
```bash
export ACCESS_ID="<your-sumologic-access-id>" ACCESS_KEY="<your-sumologic-access-key>"
examples/kup.sh
```
Check [the official docs](https://help.sumologic.com/Manage/Security/Access-Keys#manage-your-access-keys-on-preferences-page) for how to create the Sumo Logic access ID and access key

## If you already have a Keptn cluster running
1. Install Sumo Logic
```bash
export ACCESS_ID="<your-sumologic-access-id>" ACCESS_KEY="<your-sumologic-access-key>"
helm upgrade --install my-sumo sumologic/sumologic   --set sumologic.accessId="${ACCESS_ID}"   --set sumologic.accessKey="${ACCESS_KEY}"   --set sumologic.clusterName="keptn-sumo"

```
2. Install Keptn sumologic-service to integrate Sumo Logic with Keptn
```bash
export ACCESS_ID="<your-sumologic-access-id>" ACCESS_KEY="<your-sumologic-access-key>"
# cd sumologic-service
helm install sumologic-service ../helm --set sumologicservice.accessId=${ACCESS_ID} --set sumologicservice.accessKey=${ACCESS_KEY} 

```

3. Add SLI and SLO
```bash
keptn add-resource --project="<your-project>" --stage="<stage-name>" --service="<service-name>" --resource=/path-to/your/sli-file.yaml --resourceUri=sumologic/sli.yaml
keptn add-resource --project="<your-project>"  --stage="<stage-name>" --service="<service-name>" --resource=/path-to/your/slo-file.yaml --resourceUri=slo.yaml
```
Example:
```bash
keptn add-resource --project="podtatohead" --stage="hardening" --service="helloservice" --resource=./quickstart/sli.yaml --resourceUri=sumologic/sli.yaml
keptn add-resource --project="podtatohead" --stage="hardening" --service="helloservice" --resource=./quickstart/slo.yaml --resourceUri=slo.yaml
```
Check [./quickstart/sli.yaml](https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/examples/quickstart/sli.yaml) and [./quickstart/slo.yaml](https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/examples/quickstart/slo.yaml) for example SLI and SLO. 

<!-- TODO: Uncomment this after the PR to support switching SLI provider is merged -->
<!-- 4. Configure Keptn to use Sumo Logic SLI provider
Use keptn CLI version [0.15.0](https://github.com/keptn/keptn/releases/tag/0.15.0) or later.
```bash
keptn configure monitoring sumologic --project <project-name>  --service <service-name>
``` -->

5. Trigger delivery
```bash
keptn trigger delivery --project=<project-name> --service=<service-name> --image=<image> --tag=<tag>
```
Example:
```bash
keptn trigger delivery --project=podtatohead --service=helloservice --image=docker.io/jetzlstorfer/helloserver --tag=0.1.1
```
Observe the results in the [Keptn Bridge](https://keptn.sh/docs/0.15.x/bridge/)

# Not supported in the query
- `fillmissing`
- `outlier`
- `timeshift`

Why? Because the API does not support `fillmissing` and `outlier`. `timeshift` is supported but you can't write it in the query like `<my-query> | timeshift`. We plan to support `timeshift` in the future ([issue](https://github.com/vadasambar/sumologic-service/issues/1)) but support for `fillmissing` and `outlier` depends on Sumo Logic (can't do anything until Sumo Logic supports it). 

# Rules for using `quantize`
Based on https://help.sumologic.com/Metrics/Metric-Queries-and-Alerts/07Metrics_Operators/quantize#quantize-syntax
1. Use only 1 `quantize` (using `quantize` multiple times in a query leads to error)
2. Use `quantize` immediately after the metric query before any other operator
3. Quantize should be strictly defined as `query | quantize to [TIME INTERVAL] using [ROLLUP]` (this differs from how Sumo Logic quantize works. You need to be explicit here. Dropping [TIME INTERVAL] or `using` or `[ROLLUP]` won't work)  

Why so many rules? Because [Sumo Logic API does not support quantize in the query](https://api.sumologic.com/docs/#operation/runMetricsQueries). We have implemented a wrapper
which mimics quantize which works well if you adhere to 

## Compatibility Matrix

*Please fill in your versions accordingly*

| Keptn Version    | [sumologic-service Docker Image](https://github.com/keptn-sandbox/sumologic-service/pkgs/container/sumologic-service) |
|:----------------:|:----------------------------------------:|
|       0.15.0      | keptn-sandbox/sumologic-service:0.15.0 |

## Installation

```bash
export ACCESS_ID="<your-sumologic-access-id>" ACCESS_KEY="<your-sumologic-access-key>"
# cd sumologic-service
helm upgrade --install my-sumo sumologic/sumologic   --set sumologic.accessId="${ACCESS_ID}"   --set sumologic.accessKey="${ACCESS_KEY}"   --set sumologic.clusterName="keptn-sumo"

```
<!-- TODO: Uncomment this after the PR to support switching SLI provider is merged -->
<!-- Tell Keptn to use Sumo Logic as SLI provider for your project/service
```bash
keptn configure monitoring sumologic --project <project-name>  --service <service-name>
``` -->

This should install the `sumologic-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment sumologic-service -o wide
kubectl -n keptn get pods -l run=sumologic-service
```

### Deploy in your Kubernetes cluster

To deploy the current version of the *sumologic-service* in your Keptn Kubernetes cluster use the [`helm chart`](https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/chart/Chart.yaml) file,
for example:

```console
helm install -n keptn sumologic-service chart/
```

This should install the `sumologic-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment sumologic-service -o wide
kubectl -n keptn get pods -l run=sumologic-service
```

### Up- or Downgrading

Adapt and use the following command in case you want to up- or downgrade your installed version (specified by the `$VERSION` placeholder):

```bash
helm upgrade sumologic-service ./helm --set sumologicservice.accessId=${ACCESS_ID} --set sumologicservice.accessKey=${ACCESS_KEY} 
```

### Uninstall

To delete a deployed *sumologic-service* helm chart:

```bash
helm uninstall sumologic-service
```

## License

Please find more information in the [https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/LICENSE](https://raw.githubusercontent.com/keptn-sandbox/sumologic-service/release-0.15.0/LICENSE) file.
