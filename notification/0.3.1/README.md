# Keptn Notification Service

The *notification-service* is a [Keptn](https://keptn.sh) service that is responsible for sending specific events as a notification to

* MS Teams
* Slack
* Webex Teams

Read an overview of this service in action on MS teams in this blog:
[Keptn now talks MS Teams: How we expand Keptn’s footprint in the Microsoft world](https://medium.com/keptn/keptn-now-talks-ms-teams-how-we-expand-keptns-footprint-in-the-microsoft-world-c330c0c8d4f1)

Watch this short [YouTube video](https://youtu.be/T-qTVht4yI8) that demonstrates the setup and the Keptn notifications in action.

This notification service requires to be deployed into a Keptn environment and subscribes 
to the following [Keptn Cloud Events](https://github.com/keptn/spec/blob/master/cloudevents.md):

* sh.keptn.event.configuration.change
* sh.keptn.events.deployment-finished
* sh.keptn.events.tests-finished  
* sh.keptn.events.evaluation-done
* sh.keptn.events.problem

The service will send a notification to the configured notification provider (MS Teams, Slack, Webex Teams).

_**NOTE: The service will not send test-finished notification if teststrategy is empty**_

## Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Notification Service Image](https://hub.docker.com/r/keptncontrib/notification-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.5.x      | keptncontrib/notification-service:0.2.0  |
|       0.6.x      | keptncontrib/notification-service:0.3.0  |
|       0.7.x      | keptncontrib/notification-service:0.3.1  |
|      develop     | keptncontrib/notification-service:latest |

# Setup
## 1. Setup your Notification Provider

Please set up either Microsoft Teams, Slack or Webex Teams as described below.

### Microsoft Teams

All of these steps are done in Microsoft Teams client.
1. Add a new team
1. In the new team, add a new channel for the Keptn notifications. Save the new channel webhook URL
1. In the new channel, add a new connector of type Webhook
1. Others can join the channel too by first joining the team and adding the new channel

### Slack

A keptn service that forwards events on keptn channels to a Slack channel using a webhook URL. To get your Slack Webhook URL please follow the instructions here: https://api.slack.com/incoming-webhooks

### Webex Teams

1. Use an existing team or create a new team in the Webex Teams client
1. Create a new space in the team
1. Go to https://apphub.webex.com/teams/applications/incoming-webhooks-cisco-systems and login
1. Create a Webhook by giving it a name and selecting the space you created before
1. Copy the URL and insert it as described in 2.3
1. You can invite members to this space or they can join by themselves

## 2. Installation of Notification Service in Keptn

### Prerequisits
* Have a cluster with [Keptn 0.6.0](https://keptn.sh/docs/0.6.0/installation/setup-keptn/) installed
* Slack or Microsoft teams account with permission to add apps/teams/channels
* For development: Docker for running or building new images locally 

### Keptn notification service

1. Make a copy of the [deploy/notification-service.yaml](deploy/notification-service.yaml) file (Note: do not use right-click and download).
1. Ensure you are installing the correct version of the notification service and adapt 
   the `image` in **notification-service.yaml** if necessary:
    ```yaml
    containers:
    - name: notification-service
        image: keptncontrib/notification-service:0.3.1
    ```
1. Furthermore, adjust these environment variables with the webhook URL of the service you want to send notifications to. Leave the value empty if the referenced service is not being used.
    ```yaml
    - name: TEAMS_URL
    value: ""
    - name: BRIDGE_URL
    value: ""
    - name: WEBEXTEAMS_URL
    value: ""
    ```
1. Deploy services into cluster
  * ```kubectl apply -f notification-service.yaml -n keptn``` using the file in this repo
1. Now run Keptn pipelines and watch for the notifications in your team channel
1. Validate cluster resources ```kubectl -n keptn get pods```.  You should see the pod running the service.

# Send notifications

Use the keptn CLI to start a pipeline using the command [keptn send event new-artifact](https://keptn.sh/docs/0.6.0/reference/cli/#keptn-send-event-new-artifact). As the pipeline runs,
it will send various cloud events like "configuration change" and "deployment finished".