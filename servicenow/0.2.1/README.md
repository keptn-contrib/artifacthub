# ServiceNow keptn service

Small demo for showcasing how to enable runbook automation with workflows in ServiceNow with [Keptn](https://keptn.sh).

The servicenow-service is a Keptn-service that can be used for create events and update alerts in ServiceNow.

The servicenow-service listens to keptn events of type:

- sh.keptn.events.problem.open

Whenever a problem is detected by keptn, the servicenow-service will receive a sh.keptn.events.problem.open keptn event, it will then process and parse the event to then send it to the ServiceNow event API and create an alert.

## Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Prometheus Service Image](https://hub.docker.com/r/keptn/servicenow-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.4.x      | keptn/servicenow-service:0.1.3  |
|       0.5.x      | keptn/servicenow-service:0.1.4  |
|       0.6.x      | keptn/servicenow-service:0.2.0 |
|       0.7.2      | keptn/servicenow-service:0.2.1 |

## Installation

### Create ServiceNow secret

- Create a ServiceNow kubernetes secret to allow the ServiceNow keptn service to create events and update alerts in ServiceNow.

- Create a file as shown below that contains your ServiceNow credentials and save it in your current directory as cred_file.yaml:

```
SERVICENOW_INSTANCE: {instance_id}.service-now.com
SERVICENOW_USER: your_servicenow_user
SERVICENOW_PASSWORD: your_servicenow_password
```

**Note:** The ServiceNow user needs to have the evt_mgmt_integration or admin role(s) assigned to it.

- Run the command below to create the ServiceNow secret:

```
kubectl create secret generic servicenow -n keptn --from-file=servicenow-credentials=cred_file.yaml
```

### Install the ServiceNow service on the keptn namespace

- Subscribe the servicenow-service to keptn sh.keptn.event.problem.open events by applying the distributor manifest:

- Deploy the servicenow-service by running the following command:

```
kubectl apply -f deploy/service.yaml -n keptn
```

After running these commands, the servicenow-service and distributor are now deployed in your cluster. Execute the following commands to verify the deployment of the servicenow-service.

```
kubectl get svc servicenow-service -n keptn
```

```
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
servicenow-service   ClusterIP   10.51.246.134   <none>        8080/TCP   18m
```

```
kubectl get po -n keptn | grep "servicenow"
```

```
NAME                                                              READY   STATUS    RESTARTS   AGE
servicenow-service-5b67cc545c-c2452                               2/2     Running   0          17m
```

### Delete the ServiceNow service on the keptn namespace

To delete a deployed servicenow-service and distributor, use the file deploy/service.yaml from this repository and delete the Kubernetes resources:

```
kubectl delete -f deploy/service.yaml -n keptn
```