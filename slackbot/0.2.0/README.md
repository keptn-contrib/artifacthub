# Slackbot service

The *slackbot-service* is a [Keptn](https://keptn.sh) service that is responsible for interacting with Keptn via a Slack app. You can interact with the app and bot by e.g., asking for a deployment evaluation, trigger an evalution by telling the bot about a finished deployment or get notified about an approval request.

**Please note:** If you are looking for the Slack integration that **sends** events from Keptn into a Slack channel, please refer to the [notification-service](https://github.com/keptn-contrib/notification-service). The slackbot-service is for triggering actions via the Slackbot and does not serve as a notifications service.

We are going to install the service in the same cluster that Keptn is running in.
Checkout also the [installation option for Keptn on K3s](https://github.com/keptn-sandbox/keptn-on-k3s).

## Installation

### Create & install Slack app

1. Create a **[classic Slack app](https://api.slack.com/apps?new_classic_app=1)** and give it a name, e.g., **Keptn-App** and select the development slack workspace.

1. In the next screen, add bot to the app. 

    ![add bot](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/add-bot.png)

1. Add a legacy bot user to the bot. 

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/add-legacy-bot-user.png)

1. Give the Bot a name, e.g, **Keptn**. 

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/add-bot-user.png)

1. Click on **Install App** in the left menu and **Install App to Workspace**. 

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/install-app.png)

1. Confirm the next dialog.

1. Copy the **Bot User OAuth Access Token** as we will need it later. 

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/copy-bot-token.png)

1. We are finished with this integration by now. However, we need to change some settings later, so pleae keep this browser open.

1. Go to your Slack workspace and create a new channel that will receive the approval notifications. You can name it, e.g., **Keptn-approvals**. 

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/add-slack-channel.png)

1. Add the app to the channel by clicking on **Add an app** and select the newly created app from the list.

1. In the left menu of Slack right-click on the channel that you just created and click on **Copy link**. Open this link in a browser or paste it into a textfile as we will need the channel ID for the integration to work. 

1. The link will look similar to *https://your-workspace.slack.com/archives/C018WDNTZKN* - please copy the last part of the URL after the last `/` as this is the channel ID that we'll need in a minute. In this example the channel ID is `C018WDNTZKN`.

### Deploy Slackbot service

This repository comes with a manifest that will be used to install this integration to Keptn.

1. Set two environment variables as we need them later. Use the values that you have copied earlier.

    ```
    export SLACKBOT_TOKEN=xxxxxx
    export SLACK_CHANNEL=xxxxxxx
    ```

1. Create a secret with this environment variables, you can go ahead and copy/paste this next line. Make sure you are connected to the correct Kubernetes cluster.

    ```
    kubectl create secret generic slackbot --from-literal="slackbot-token=$SLACKBOT_TOKEN" --from-literal="slack-channel=$SLACK_CHANNEL" -n keptn
    ```    

1. Apply the deployment file from this repo by first cloning the repo and then applying the file.

    ```
    git clone https://github.com/keptn-sandbox/slackbot-service
    ```


    Please note that if you want to have the integration with the Keptn's bridge enabled (which is strongly recommended) - first edit this file and put the Keptn's Bridge URL in the corresponding line in the `env` section of the manifest.
    ```yaml
    ...
    env:
    - name: keptn_host
    value: "http://api-gateway-nginx.keptn.svc.cluster.local"
    - name: bridge_url
    value: "" # add your URL here
    - name: keptn_api_token
    valueFrom:
        secretKeyRef:
        name: keptn-api-token
        key: keptn-api-token
    ...
    ```

    Apply the manifest.
    ```
    kubectl apply -f slackbot-service/deploy/slackbot-service.yaml
    ```

1. Fetch the **EXTERNAL-IP** of the `slackbot-service` that we are going to need for the two-way integration with Slack.
    ```
    kubectl get svc slackbot-external -n keptn

    NAME                TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)        AGE
    slackbot-external   LoadBalancer   10.0.11.178   34.67.190.13   80:31016/TCP   1h
    ```

1. Go back to your browser if you still have Slack app open or navigate to the [Slack app overview](https://api.slack.com/apps/) and select the Slack app that we created earlier.

1. Click on **Interactivity & Shortcuts** and activate the toggle. Add a **Request URL** add the URL of the public enpoint appended with `handler` for your Slackbot service. Example: `http://34.67.190.1/handler`

    ![](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/add-interactivity.png)

1. Click on **Save Changes**.

1. Now, whenever there is a new approval request you will be notified in your Slack channel and can approve or decline the request directly via Slack, either on your desktop or mobile device!

### Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Slackbot Service Image](https://hub.docker.com/r/keptncontrib/slackbot-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.6.x      | keptncontrib/slackbot-service:0.1.0  |
|       0.7.x      | keptncontrib/slackbot-service:0.2.0  |

## Usage

- Ask the bot what you can do:

    ![help](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/demo-help.png)

- Ask the bot for the already created projects:

    ![help](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/demo-projects.png)

- Ask the bot to start the evaluation and the bot will return the result once it is ready.
    ![usage](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/demo-usage.png)

- The bot will post into the Slack channel once there is a new approval request:
    ![approval request](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/app-approval.png)

    Once the request is approved, the message will update:
    ![approval done](https://raw.githubusercontent.com/keptn-sandbox/slackbot-service/master/images/app-approved.png)