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

