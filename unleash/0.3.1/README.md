# Unleash Service

This service allows to interact with the open source feature toggle system [unleash](https://github.com/unleash). 
Triggered by a Keptn CloudEvent of the type `sh.keptn.event.action.triggered`. After the features specified in the event 
have been toggled, it sends out an `sh.keptn.event.action.finished` event.

Example payload for an action.triggered event:

```
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

## Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Unleash Service Image](https://hub.docker.com/r/keptncontrib/unleash-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.6.x      | keptncontrib/unleash-service:0.1.0  |
|       0.7.x      | keptncontrib/unleash-service:0.2.0  |
|       0.8.x      | keptncontrib/unleash-service:0.3.0  |
|       0.8.x      | keptncontrib/unleash-service:0.3.1  |


## Installation

To deploy the `unleash-service` in version 0.3.1, execute the following command:

```
kubectl apply -f https://github.com/keptn-contrib/unleash-service/tree/release-0.3.1/deploy/service.yaml -n keptn
```

## Uninstall the unleash-service

To uninstall the service, execute:

```
kubectl delete -f https://github.com/keptn-contrib/unleash-service/tree/release-0.3.1/deploy/service.yaml -n keptn
```

