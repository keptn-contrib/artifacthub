# ServiceNow keptn service

Whenever a remediaton action of type `trigger-servicenow-flow` is triggered by keptn, the `servicenow-service` will receive a keptn event of type `sh.keptn.event.action.triggered`. Based on the remediation configuration, the service can trigger any ServiceNow `flow` that has a [REST API trigger] with an arbitrary set of values which will be passed on to the ServiceNow API endpoint along with the `sh.keptn.event.action.triggered` event payload. After the ServiceNow action has finished running, it sends out a `sh.keptn.event.action.finished` event. By default the servicenow-service will also include the JSON payload of event `sh.keptn.event.action.triggered` when triggering the flow.

Example of an action triggered event:

```json
{
    "type": "sh.keptn.event.action.triggered",
    "specversion": "0.2",
    "source": "https://github.com/keptn/keptn/remediation-service",
    "id": "f2b878d3-03c0-4e8f-bc3f-454bc1b3d79d",
    "time": "2019-06-07T07:02:15.64489Z",
    "contenttype": "application/json",
    "shkeptncontext": "08735340-6f9e-4b32-97ff-3b6c292bc509",
    "data": {
        "action": {
            "name": "CreateIncident",
            "action": "trigger-servicenow-flow",
            "description": "Creates a ServiceNow incident",
            "value": {
                "flowApiPath": "/api/dynat/keptn_create_incident",
                "httpMethod": "POST",
                "retries": 10
            }
        },
        "problem": {
            "ImpactedEntity": "carts-primary",
            "PID": "93a5-3fas-a09d-8ckf",
            "ProblemDetails": "Process name",
            "ProblemID": "762",
            "ProblemTitle": "cpu_usage_sockshop_carts",
            "State": "OPEN"
        },
        "project": "sockshop",
        "service": "carts",
        "stage": "staging",
        "labels": {
            "testId": "4711",
            "buildId": "build-17",
            "owner": "JohnDoe"
        }
    }
}
```

Remediation Config Example:

```yaml
apiVersion: spec.keptn.sh/0.1.4
kind: Remediation
metadata:
  name: carts-remediation
spec:
  remediations:
    - problemType: High CPU Usage
      actionsOnOpen:
        - action: trigger-servicenow-flow
          name: Trigger ServiceNow Flow
          description: Creates a ServiceNow incident
          value:
            flowApiPath: /api/dynat/keptn_create_incident # mandatory parameter
            httpMethod: POST # mandatory parameter
            retries: 10
```

## Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.

| Keptn Version    | [ServiceNow Service Image](https://hub.docker.com/r/keptncontrib/servicenow-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.4.x      | keptn/servicenow-service:0.1.3  |
|       0.5.x      | keptn/servicenow-service:0.1.4  |
|       0.6.x      | keptn/servicenow-service:0.2.0  |
|       0.7.x      | keptn/servicenow-service:0.2.1  |
|      0.8.0-0.3   | keptn/servicenow-service:0.3.0  |