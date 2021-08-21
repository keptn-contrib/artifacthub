# Unleash Service

This service allows to interact with the open source feature toggle system [unleash](https://github.com/unleash). 
Triggered by a Keptn CloudEvent of the type `sh.keptn.event.action.triggered`. After the features specified in the event have been toggled, it sends out an `sh.keptn.event.action.finished` event.

Example payload for an action.triggered event:

```json
{
  "type": "sh.keptn.event.action.triggered",
  "specversion": "1.0",
  "source": "keptn-user",
  "id": "f2b878d3-03c0-4e8f-bc3f-454bc1b3d79d",
  "time": "2019-06-07T07:02:15.64489Z",
  "contenttype": "application/json",
  "shkeptncontext": "08735340-6f9e-4b32-97ff-3b6c292bc509",
  "data": {
    "action": {
      "name": "FeatureToggle",
      "action": "toggle-feature",
      "description": "toggle a feature",
      "values": {
        "EnableItemCache": "on"
      }
    },
    "problem": {
      "ImpactedEntity": "carts-primary",
      "PID": "93a5-3fas-a09d-8ckf",
      "ProblemDetails": "Pod name",
      "ProblemID": "762",
      "ProblemTitle": "cpu_usage_sockshop_carts",
      "State": "OPEN"
    },
    "project": "sockshop",
    "stage": "staging",
    "service": "carts",
    "labels": {
      "testid": "12345",
      "buildnr": "build17",
      "runby": "JohnDoe"
    }
  }
}
```