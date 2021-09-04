# Prometheus Service

The *prometheus-service* is a [Keptn](https://keptn.sh) service that is responsible for

1. configuring Prometheus for monitoring services managed by Keptn, and
2. receiving alerts from Prometheus Alertmanager and translating the alert payload to a cloud event that is sent to the Keptn API.
3. It's used for retrieving Service Level Indicators (SLIs) from a Prometheus API endpoint. Per default, it fetches metrics from the prometheus instance set up by Keptn
   (`prometheus-service.monitoring.svc.cluster.local:8080`), but it can also be configured to use any reachable Prometheus endpoint using basic authentication by providing the credentials
   via a secret in the `keptn` namespace of the cluster.

    The supported default SLIs are:
    
    - throughput
    - error_rate
    - response_time_p50
    - response_time_p90
    - response_time_p95

The provided SLIs are based on the [RED metrics](https://grafana.com/files/grafanacon_eu_2018/Tom_Wilkie_GrafanaCon_EU_2018.pdf)

## Compatibility Matrix

Please always double-check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Prometheus Service Image](https://hub.docker.com/r/keptncontrib/prometheus-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.5.x      | keptncontrib/prometheus-service:0.2.0  |
|       0.6.x      | keptncontrib/prometheus-service:0.3.0  |
|       0.6.1      | keptncontrib/prometheus-service:0.3.2  |
|       0.6.2      | keptncontrib/prometheus-service:0.3.4  |
|   0.7.0, 0.7.1   | keptncontrib/prometheus-service:0.3.5  |
|       0.7.2      | keptncontrib/prometheus-service:0.3.6  |
|   0.8.0-alpha    | keptncontrib/prometheus-service:0.4.0-alpha  |
|   0.8.0          | keptncontrib/prometheus-service:0.4.0  |
|   0.8.1, 0.8.2   | keptncontrib/prometheus-service:0.5.0  |
|   0.8.1 - 0.8.3  | keptncontrib/prometheus-service:0.6.0  |
|   0.8.4 - 0.8.7  | keptncontrib/prometheus-service:0.6.1  |

## Setup Prometheus Monitoring

Keptn doesn't install or manage Prometheus and its components. Users need to install Prometheus and Prometheus Alert manager as a prerequisite.

Some environment variables have to set up in the prometheus-service deployment
```yaml
    # Prometheus installed namespace
    - name: PROMETHEUS_NS
      value: 'default'
    # Prometheus server configmap name
    - name: PROMETHEUS_CM
      value: 'prometheus-server'
    # Prometheus server app labels
    - name: PROMETHEUS_LABELS
      value: 'component=server'
    # Prometheus configmap data's config filename
    - name: PROMETHEUS_CONFIG_FILENAME
      value: 'prometheus.yml'
    # AlertManager configmap data's config filename
    - name: ALERT_MANAGER_CONFIG_FILENAME
      value: 'alertmanager.yml'
    # Alert Manager config map name
    - name: ALERT_MANAGER_CM
      value: 'prometheus-alertmanager'
    # Alert Manager app labels
    - name: ALERT_MANAGER_LABELS
      value: 'component=alertmanager'
    # Alert Manager installed namespace
    - name: ALERT_MANAGER_NS
      value: 'default'
    # Alert Manager template configmap name
    - name: ALERT_MANAGER_TEMPLATE_CM
      value: 'alertmanager-templates'
```

