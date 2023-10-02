# Keptn Notification Service
![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-contrib/notification-service)
[![Build Status](https://travis-ci.org/keptn-contrib/notification-service.svg?branch=master)](https://travis-ci.org/keptn-contrib/notification-service)

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

1. Make a copy of the [https://raw.githubusercontent.com/keptn-contrib/notification-service/release-0.3.0/deploy/notification-service.yaml](https://raw.githubusercontent.com/keptn-contrib/notification-service/release-0.3.0/deploy/notification-service.yaml) and [https://raw.githubusercontent.com/keptn-contrib/notification-service/release-0.3.0/deploy/notification-distributors.yaml](https://raw.githubusercontent.com/keptn-contrib/notification-service/release-0.3.0/deploy/notification-distributors.yaml) files (Note: do not use right-click and download).
1. Ensure you are installing the correct version of the notification service and adapt 
   the `image` in **notification-service.yaml** if necessary:
    ```yaml
    containers:
    - name: notification-service
        image: keptncontrib/notification-service:0.3.0.beta
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
  * ```kubectl apply -f notification-service.yaml``` using the new service Helm Chart file
  * ```kubectl apply -f notification-distributors.yaml``` using the file in this repo
1. Now run Keptn pipelines and watch for the notifications in your team channel
1. Validate cluster resources ```kubectl -n keptn get pods```.  You should see service and distributor pods.

# Send notifications

Use the keptn CLI to start a pipeline using the command [keptn send event new-artifact](https://keptn.sh/docs/0.6.0/reference/cli/#keptn-send-event-new-artifact).   As the pipeline runs,
it will send various cloud events like "configuration change" and "deployment finished"

# Local development

## Build and run the application
1. Clone this repo
1. Run ```npm install``` to get all the requires modules
1. Start the service with ```npm run start:dev```.  This will update "on-the-fly" as you make file changes
1. Access the service at ```http://localhost:8080```

## Testing

You can use the PostMan collection JSON file ```keptn-notifications.postman_collection.json``` in this repo to test all the events.

To manually setup a request in a tool like Postman, use the following values.
* URL = ```http://localhost:8080```
* Content-Type = application/cloudevents+json
* Type = POST
* Raw Body for a Keptn deployment event
    ```
    {
        "type": "sh.keptn.event.configuration.change",
        "specversion": "0.2",
        "source": "https://github.com/keptn/keptn/cli",
        "id": "49ac0dec-a83b-4bc1-9dc0-1f050c7e781b",
        "time": "2019-06-07T07:02:15.64489Z",
        "contenttype": "application/json",
        "shkeptncontext":"49ac0dec-a83b-4bc1-9dc0-1f050c7e789b",
        "data": {
            "project": "sockshop",
            "stage": "staging",
            "service": "carts",
            "valuesCanary": {
            "image": "docker.io/keptnexamples/carts:0.9.1"
            }
        }
    }
    ```
You should get a HTTP 200 response code and see the notification in either Slack or Microsoft Teams.

## Build a Docker image and run as a container

1. Run these commands after adjusting the repo, image name, and tag in this example
    ```
    # build image
    docker build -t keptncontrib/notification-service:dev .

    # start image. Leave out environment variable for unwanted service
    docker run -p 8080:8080 -e TEAMS_URL="<Your URL>" -e SLACK_URL="your URL" keptncontrib/notification-service:dev
    ```
1. Access the service at ```http://localhost:8080```


# Contributions

You are welcome to contribute using Pull Requests against the **master** branch. Before contributing, please read our [Contributing Guidelines](https://raw.githubusercontent.com/keptn-contrib/notification-service/release-0.3.0/CONTRIBUTING.md).


# Travis-CI setup

Travis is configured with CI to automatically build docker images for pull requests and commits. The  pipeline can be viewed at https://travis-ci.org/keptn-contrib/notification-service.

The travis pipeline needs to be configured with the `REGISTRY_USER` and `REGISTRY_PASSWORD` variables. 

# Reference

## Microsoft cards
* https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference
* https://www.lee-ford.co.uk/send-message-cards-with-microsoft-teams/
