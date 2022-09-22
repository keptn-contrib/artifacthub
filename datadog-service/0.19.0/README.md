# datadog-service
![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-sandbox/datadog-service)
[![Go Report Card](https://goreportcard.com/badge/github.com/keptn-sandbox/datadog-service)](https://goreportcard.com/report/github.com/keptn-sandbox/datadog-service)

This implements the `datadog-service` that integrates the [Datadog](https://en.wikipedia.org/wiki/Datadog) observability platform with Keptn. This enables you to use Datadog as the source for the Service Level Indicators ([SLIs](https://keptn.sh/docs/0.19.x/reference/files/sli/)) that are used for Keptn [Quality Gates](https://keptn.sh/docs/concepts/quality_gates/).
If you want to learn more about Keptn visit us on [keptn.sh](https://keptn.sh)

Check the issue on the main repo for more info: https://github.com/keptn/keptn/issues/2652


## Quickstart
If you are on Mac or Linux, you can use [examples/kup.sh](https://raw.githubusercontent.com/keptn-sandbox/datadog-service/release-0.19.0/examples/kup.sh) to set up a local Keptn installation that uses Datadog. This script creates a local minikube cluster, installs Keptn, Istio, Datadog and the Datadog integration for Keptn (check the script for pre-requisites). 

To use the script,
```bash
export DD_API_KEY="<your-datadog-api-key>" DD_APP_KEY="<your-datadog-app-key>" DD_SITE="datadoghq.com" 
examples/kup.sh
```
Check [the official docs](https://docs.datadoghq.com/account_management/api-app-keys/) for how to create the Datadog API key and Application key

Note: Application keys get the same permissions as you. You might want to narrow down the permissions (datadog-service only reads metrics from the API. Check the official docs linked above for more information).

## If you already have a Keptn cluster running
1. Install datadog
```bash
export DD_API_KEY="<your-datadog-api-key>" DD_APP_KEY="<your-datadog-app-key>" DD_SITE="datadoghq.com" 
helm install datadog --set datadog.apiKey=${DD_API_KEY} datadog/datadog --set datadog.appKey=${DD_APP_KEY} --set datadog.site=${DD_SITE} --set clusterAgent.enabled=true --set clusterAgent.metricsProvider.enabled=true --set clusterAgent.createPodDisruptionBudget=true --set clusterAgent.replicas=2

```
2. Install Keptn datadog-service to integrate Datadog with Keptn
```bash
export DD_API_KEY="<your-datadog-api-key>" DD_APP_KEY="<your-datadog-app-key>" DD_SITE="datadoghq.com" 
# cd datadog-service
helm install datadog-service ./helm --set datadogservice.ddApikey=${DD_API_KEY} --set datadogservice.ddAppKey=${DD_APP_KEY} --set datadogservice.ddSite=${DD_SITE}
```

3. Add SLI and SLO
```bash
keptn add-resource --project="<your-project>" --stage="<stage-name>" --service="<service-name>" --resource=/path-to/your/sli-file.yaml --resourceUri=datadog/sli.yaml
keptn add-resource --project="<your-project>"  --stage="<stage-name>" --service="<service-name>" --resource=/path-to/your/slo-file.yaml --resourceUri=slo.yaml
```
Example:
```bash
keptn add-resource --project="podtatohead" --stage="hardening" --service="helloservice" --resource=./quickstart/sli.yaml --resourceUri=datadog/sli.yaml
keptn add-resource --project="podtatohead" --stage="hardening" --service="helloservice" --resource=./quickstart/slo.yaml --resourceUri=slo.yaml
```
Check [./quickstart/sli.yaml](https://raw.githubusercontent.com/keptn-sandbox/datadog-service/release-0.19.0/examples/quickstart/sli.yaml) and [./quickstart/slo.yaml](https://raw.githubusercontent.com/keptn-sandbox/datadog-service/release-0.19.0/examples/quickstart/slo.yaml) for example SLI and SLO. 

4. Configure Keptn to use datadog SLI provider
Use keptn CLI version [0.15.0](https://github.com/keptn/keptn/releases/tag/0.15.0) or later.
```bash
keptn configure monitoring datadog --project <project-name>  --service <service-name>
```

5. Trigger delivery
```bash
keptn trigger delivery --project=<project-name> --service=<service-name> --image=<image> --tag=<tag>
```
Example:
```bash
keptn trigger delivery --project=podtatohead --service=helloservice --image=docker.io/jetzlstorfer/helloserver --tag=0.1.1
```
Observe the results in the [Keptn Bridge](https://keptn.sh/docs/0.19.x/bridge/)
## Compatibility Matrix

*Please fill in your versions accordingly*

| Keptn Version    | [datadog-service Docker Image](https://github.com/keptn-sandbox/datadog-service/pkgs/container/datadog-service) |
|:----------------:|:----------------------------------------:|
|       0.11.4      | ghcr.io/keptn-sandbox/datadog-service:0.1.0 |
|       0.11.4      | ghcr.io/keptn-sandbox/datadog-service:0.2.0 |
|       0.15.0      | ghcr.io/keptn-sandbox/datadog-service:0.15.0 |
|       0.16.0      | ghcr.io/keptn-sandbox/datadog-service:0.16.0 |
|       0.17.0      | ghcr.io/keptn-sandbox/datadog-service:0.17.0 |
|       0.18.1      | ghcr.io/keptn-sandbox/datadog-service:0.18.1 |
|       0.19.0      | ghcr.io/keptn-sandbox/datadog-service:0.19.0 | 

datadog-service version will match Keptn version starting from 0.15.0 version of Keptn e.g., datadog-service 0.15.x is compatible with Keptn 0.15.x 

## Installation

```bash
export DD_API_KEY="<your-datadog-api-key>" DD_APP_KEY="<your-datadog-app-key>" DD_SITE="datadoghq.com" 
# cd datadog-service
helm install datadog-service ./helm --set datadogservice.ddApikey=${DD_API_KEY} --set datadogservice.ddAppKey=${DD_APP_KEY} --set datadogservice.ddSite=${DD_SITE}
```
Tell Keptn to use datadog as SLI provider for your project/service
```bash
keptn configure monitoring datadog --project <project-name>  --service <service-name>
```

This should install the `datadog-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment datadog-service -o wide
kubectl -n keptn get pods -l run=datadog-service
```
### Up- or Downgrading

Adapt and use the following command in case you want to up- or downgrade your installed version (specified by the `$VERSION` placeholder):

```bash
helm upgrade datadog-service ./helm --set datadogservice.ddApikey=${DD_API_KEY} --set datadogservice.ddAppKey=${DD_APP_KEY} --set datadogservice.ddSite=${DD_SITE}
```

### Uninstall

To delete a deployed *datadog-service* helm chart:

```bash
helm uninstall datadog-service
```

## Known problems
1. If the evaluation window of the query is too short, the api might return an empty result which datadog-service treats as 0 and fails the evaluation. [Issue](https://github.com/keptn-sandbox/datadog-service/issues/10)
2. There is an on-purpose 60s delay before the datadog metrics API is called. This is because, calling the metrics API earlier leads to incorrect data. [Issue](https://github.com/keptn-sandbox/datadog-service/issues/8)
3. Does not support default queries for throughput, error rate, request latency etc., i.e., you have to enter the entire query. [Issue](https://github.com/keptn-sandbox/datadog-service/issues/9)

## License

Please find more information in the [https://raw.githubusercontent.com/keptn-sandbox/datadog-service/release-0.19.0/LICENSE](https://raw.githubusercontent.com/keptn-sandbox/datadog-service/release-0.19.0/LICENSE) file.