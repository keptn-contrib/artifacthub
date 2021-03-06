# Dynatrace Service

![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-contrib/dynatrace-service)
[![Build Status](https://travis-ci.org/keptn-contrib/dynatrace-service.svg?branch=master)](https://travis-ci.org/keptn-contrib/dynatrace-service)
[![Go Report Card](https://goreportcard.com/badge/github.com/keptn-contrib/dynatrace-service)](https://goreportcard.com/report/github.com/keptn-contrib/dynatrace-service)

The *dynatrace-service* is a [Keptn-service](https://keptn.sh) that forwards Keptn events - occurring during a delivery workflow - to Dynatrace. In addition, the service is responsible for configuring your Dynatrace tenant to fully interact with the Keptn installation.
 
The service is subscribed to the following [Keptn CloudEvents](https://github.com/keptn/spec/blob/master/cloudevents.md):

- sh.keptn.events.deployment-finished
- sh.keptn.events.evaluation-done
- sh.keptn.events.tests-finished
- sh.keptn.internal.event.project.create
- sh.keptn.event.monitoring.configure
- sh.keptn.event.get-sli.triggered

The *dynatrace-service* is a [Keptn](https://keptn.sh) service that is responsible for retrieving the values of SLIs from your Dynatrace Tenant via the Dynatrace Metrics v2 API endpoint. For that it handles the Keptn Event *sh.keptn.internal.event.get-sli* which gets sent as part of a quality gate evaluation!

The *dynatrace-service* provides the capabilty to connect to different Dynatrace Tenants for your Keptn projects, stages or services. It also allows you to either define SLIs through `sli.yaml` files or through a Dynatrace dashboard and all of this is configurable through `dynatrace.conf.yaml`:

![](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/images/dynatraceserviceoverview.png)

By default, even if you do not specify a custom `sli.yaml` or a Dynatrace dashboard, the following SLIs are automatically supported in case you reference them in your `slo.yaml`:

```yaml
 - throughput: builtin:service.requestCount.total
 - error_rate: builtin:service.errors.total.rate
 - response_time_p50: builtin:service.response.time:percentile(50)
 - response_time_p90: builtin:service.response.time:percentile(90)
 - response_time_p95: builtin:service.response.time:percentile(95)
```

By default these metrics (SLIs) are queried from a Dynatrace-monitored service entity with the tags `keptn_project`, `keptn_service`, `keptn_stage` & `keptn_deployment`.
![](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/images/defaultdynatracetags.png)

As highlighted above, the *dynatrace-service* also provides the following capabilities:

* Connecting to different Dynatrace Tenants (SaaS or Managed) depending on Keptn Project, Stage or Service

* Defining a custom list of SLIs based on the Dynatrace Metrics API v2. This allows SLIs to reference any metric in Dynatrace: Application, Service, Process Groups, Host, Custom Devices, Calculated Service Metrics, External Metrics ...

* Visually defining SLIs & SLOs through a Dynatrace Dashboard instead of `sli.yaml` and `slo.yaml`

## Compatibility Matrix

| Keptn Version    | [Dynatrace Service](https://hub.docker.com/r/keptncontrib/dynatrace-service/tags?page=1&ordering=last_updated) | Kubernetes Versions                      |
|:----------------:|:----------------------------------------:|:----------------------------------------:|
|       0.6.1      | keptn/dynatrace-service:0.6.2            | 1.13 - 1.15                              |
|       0.6.1      | keptncontrib/dynatrace-service:0.6.9     | 1.13 - 1.15                              |
|       0.6.2      | keptncontrib/dynatrace-service:0.7.1     | 1.13 - 1.15                              |
|       0.7.0      | keptncontrib/dynatrace-service:0.8.0     | 1.14 - 1.18                              |
|       0.7.1      | keptncontrib/dynatrace-service:0.9.0     | 1.14 - 1.18                              |
|       0.7.2      | keptncontrib/dynatrace-service:0.10.0     | 1.14 - 1.18                             |
|       0.7.3      | keptncontrib/dynatrace-service:0.10.1     | 1.14 - 1.18                            |
|       0.7.3      | keptncontrib/dynatrace-service:0.10.2     | 1.14 - 1.18                            |
|       0.7.3      | keptncontrib/dynatrace-service:0.10.3     | 1.14 - 1.18                            |
|       0.8.0, 0.8.1      | keptncontrib/dynatrace-service:0.11.0 (*)    | 1.14 - 1.19                            |
|       0.8.0, 0.8.1      | keptncontrib/dynatrace-service:0.12.0    | 1.14 - 1.19                            |
|       0.8.0 - 0.8.3     | keptncontrib/dynatrace-service:0.13.1    | 1.14 - 1.19                            |
|       0.8.0 - 0.8.3     | keptncontrib/dynatrace-service:0.14.0    | 1.14 - 1.19                            |
|       0.8.4 - 0.8.6     | keptncontrib/dynatrace-service:0.15.0    | 1.15 - 1.20                        |
|       0.8.4 - 0.8.6     | keptncontrib/dynatrace-service:0.15.1    | 1.15 - 1.20                        |
|       0.8.4 - 0.8.7     | keptncontrib/dynatrace-service:0.16.0    | 1.15 - 1.20                        |
|       0.8.4 - 0.9.2     | keptncontrib/dynatrace-service:0.17.0    | 1.15 - 1.20                        |
|       0.8.4 - 0.9.2     | keptncontrib/dynatrace-service:0.17.1    | 1.15 - 1.20                        |
|       0.10.0            | keptncontrib/dynatrace-service:0.18.0    | 1.16 - 1.21                        |
|       0.10.0            | keptncontrib/dynatrace-service:0.18.1    | 1.16 - 1.21                        |


(*) *Note:* 0.11.0 is feature-complete with 0.10.0. Changes and fixes made from 0.10.1 to 0.10.3 will be incorporated in 0.12.0

## Upgrade to 0.18.0

If you are planning to upgrade to *dynatrace-service* version `0.18.0` from a previous version, then please make sure to read and follow [these instructions on patching your secrets](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/patching-dynatrace-secrets.md) before doing the upgrade.


## Overview
- [Installation](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/installation.md)
  - [Installation](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/installation/installation.md)
  - [Up- or Downgrading](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/installation/up-or-downgrading.md)
  - [Uninstall](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/installation/uninstall.md)

- [Configuration](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/configuration.md)
  - [Sending Events to Dynatrace Monitored Entities](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/configuration/sending-events-to-dynatrace-monitored-entities.md)
  - [Synchronizing Service Entities detected by Dynatrace](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/configuration/synchronizing-service-entities-detected-by-dynatrace.md)
  - [Sending Dynatrace Problems to Keptn for Auto-Remediation](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/configuration/sending-dynatrace-problems-to-keptn-for-auto-remediation.md)

- [SLI and SLO configuration](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration.md)
  - [Configurations of Dashboard SLI/SLO queries through `dynatrace.conf.yaml`](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration/configuration-of-dashboard-sli-slo-queries.md)
  - [SLI Configuration](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration/sli-configuration.md)
  - [SLIs & SLOs for Problem Remediation](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration/slis-and-slos-for-problem-remediation.md)
  - [SLIs & SLOs via Dynatrace Dashboard](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration/slis-and-slos-via-dynatrace-dashboard.md)
  - [Known Limitations](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/sli-configuration/known-limitations.md)

- [Development](https://raw.githubusercontent.com/keptn-contrib/dynatrace-service/release-0.18.1/documentation/development.md)





