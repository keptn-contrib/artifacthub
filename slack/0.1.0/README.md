# Slack Webhook Integration

<!-- 

This is the first example of a Webhook Integration for Keptn. It should work as a template for others that follow. 

A Webhook Integration description has to contain: 
- Prerequisites 
- Configure Keptn for the Webhook call

-->

This integration shows you how to send notifications to Slack leveraging [Keptn's Webhook capabilities](https://keptn.sh/docs/0.10.x/integrations/webhooks/).

[WATCH THIS VIDEO TUTORIAL](https://www.youtube.com/watch?v=0vJS7ecayGw&t=7s) to see this in action.

Here is a quick overview of how those messages in Slack can look like (message content and format can be customized):
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/slack/0.1.0/images/slack-notifications.png)

<!-- Prerequisites describe the way of creating the Webhook at the target tooling. -->

## Prerequisites 

### Step 1: Enable Incoming Webhooks in Slack

In Slack, please follow the guidelines to enable [Incoming Webhooks](https://api.slack.com/messaging/webhooks).

### Step 2: Configure your Slack Incoming Webhook URL

Now configure your incoming webhook and obtain your webhook URL. Please be aware that the last part of the webhook URL - the X... in the given example - is sensitive data. If this data is known by other parties, they can exploit your webhook to send messages to your Slack channel.

```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

What we will later do is store that unique secret part in a Keptn secret to keep it hidden.

### Step 3: Create Slack Channels to push notifications to

In this example, we assume you have Slack channels with the name pattern PROJECT--SERVICE where PROJECT refers to the *Keptn Project name* and SERVICE to the *Service name* in your Keptn project. You can change this however if you want to by customizing the JSON Payload to the Slack Webhook.

### (Optional) Validate you have Keptn Webhook Service deployed

Keptn Webhook Service was introduced with **Keptn 0.10.0** and is getting installed by default on the Control Plane. IFfyou manually installed Keptn or upgraded manually, please validate and ensure that your Keptn installation runs the Keptn `webhook-service`.

## Configure Keptn for Slack Webhook

### Step 1: Create Keptn Secret for Slack

To secure the sensitive data of your webhook URL, a secret needs to be created:

* In Keptn, select a project then click on **Uniform page** > **Secrets** and click the **Add Secret**
* Then create a new secret with the following values:

  * *Name:* `slack-webhook`
  * *Scope:* `keptn-webhook-service`

* And the following two key-value pairs:
```
token: T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
bridgeUrl: https://your.keptn.URL
```

For reference, here is a screenshot of that secret:

![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/slack/0.1.0/images/secret-configuration.png)

### Step 2: Subscribe to a Keptn event to push notifications to Slack

To create a webhook integration, a subscription needs to be created:

* In Keptn, navigate to **Uniform page** -> **Uniform** and there select the **webhook-service**
* Click the **Add subscription** button, to create a new event subscription on the currently selected project.

**Example 1: Evaluation Finished Notifications**

* In the *Create subscription* form section, fill out the following fields:
  * *Task:* `evaluation`
  * *Task suffix:* `finished`

* In the *Webhook configuration* form section fill out the following:
  * *Request Method*: POST
  * *URL*: `https://hooks.slack.com/services/{{.secret.slack-webhook.token}}`
  * *Payload*:
  ```
  payload={ 
    "channel" : "{{.data.project}}--{{.data.service}}",
    "username" : "keptn", 
    "blocks": [
      {
        "type" : "section",
        "text" : {
          "type": "mrkdwn",
          "text" : "*Keptn Evaluation finished:* {{.data.result}} ({{.data.evaluation.score}} / 100)"
        }
      },
      {
        "type" : "section",
        "text" : {
          "type": "mrkdwn",
          "text" : "*Project:* {{.data.project}}\n*Stage:* {{.data.stage}}\n*Service:* {{.data.service}}\n*Details:* {{.secret.slack-webhook.bridgeUrl}}/bridge/evaluation/{{.shkeptncontext}}"
        }
      }
    ]
  }
  ```

* (optional) You can enrich and customize the message with event data described [here](https://keptn.sh/docs/0.10.x/integrations/webhooks/#customize-request-payload).

* Finally, click **Create subscription** to save and enable the webhook for your Slack integration.

* Here is a screenshot for your reference:
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/slack/0.1.0/images/evaluation-finished-subscription.png)

**Example 2: Deployment Finished Notifications**

This is an example for sending a deployment finished event. 

* In the *Create subscription* form section, fill out the following fields:
  * *Task:* `deployment`
  * *Task suffix:* `finished`

* In the *Webhook configuration* form section fill out the following:
  * *Request Method*: POST
  * *URL*: `https://hooks.slack.com/services/{{.secret.slack-webhook.token}}`
  * *Payload*:
  ```
  payload={
    "channel" : "{{.data.project}}--{{.data.service}}",
    "username" : "keptn", 
    "blocks": [
      {
        "type" : "section",
        "text" : {
          "type": "mrkdwn",
          "text" : "*Keptn Deployment finished:* {{.data.result}}"
        }
      },
      {
        "type" : "section",
        "text" : {
          "type": "mrkdwn",
          "text" : "*Project:* {{.data.project}}\n*Stage:* {{.data.stage}}\n*Service:* {{.data.service}}\n*URL:* {{index .data.deployment.deploymentURIsPublic 0}}\n*Details:* {{.secret.slack-webhook.bridgeUrl}}/trace/{{.shkeptncontext}}"
        }
      }
    ]
  }
  ```

* Finally, click **Create subscription** to save and enable the webhook for your Slack integration.

## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)

## Troubleshooting

* The Slack Incoming Webhook URL created by the Slack admin is specific to a single user and a single channel. If an existing webhook is tied to an account that is no longer active, the webhook URL will be invalid, the integration will be broken, and you will no longer receive messages on that Slack channel. This could be the case when you have a working webhook URL and an account is removed from Slack. If this occurs, the Slack admin will need to generate a new webhook URL using a valid account and channel. Once a new URL is generated, update the webhook URL in the event subscription.
