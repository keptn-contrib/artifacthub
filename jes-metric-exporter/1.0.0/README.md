# Metric Exporter

![metrics exported to prometheus](https://github.com/keptn-contrib/artifacthub/raw/main/jes-metric-exporter/1.0.0/assets/_metrics.jpg)

![metrics exported to dynatrace](https://github.com/keptn-contrib/artifacthub/raw/main/jes-metric-exporter/1.0.0/assets/prom_metrics.jpg)

This repository shows how to push metrics from a Keptn job executor service run to Observability backends such as **Prometheus** or **Dynatrace**.

Often you will run an existing container / tool with the job executor service which outputs results. Most likely you want to use these metrics in a subsequent Keptn task (eg. a quality gate evaluation). To do so, you will need to push the metrics to a metric backend. This repository demonstrates how this can be done.

Instructions here: `https://github.com/agardnerit/jes-metric-exporter`