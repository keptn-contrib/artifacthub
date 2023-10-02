> This integration is for Keptn v1. It is no longer supported.
>
> Users are advised to use Keptn instead: https://keptn.sh

# AWS App Runner Integration

Keptn can integrate with AWS App Runner in 3 ways:

1. Fire-and-forget triggering of App Runner from Keptn
2. Fire-and-wait triggering of App Runner from Keptn
3. Trigger Keptn from App Runner


# Fire and Forget Trigger App Runner

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/awsapprunner/1.0.0/assets/fire-and-forget-sequence.svg)

This is the most basic integration. Trigger AppRunner from a Keptn task event.

The Keptn [webhook service](https://github.com/keptn/keptn/tree/master/webhook-service) is used to listen for the relevant task event and trigger the App Runner endpoint. Configure the [webhook service](https://github.com/keptn/keptn/tree/master/webhook-service) to send the finished event automatically.

The webhook service will:

1. Listen for your event (usually a `task.triggered` event)
1. Send a `task.started` event back to Keptn automatically
1. Trigger AppRunner
1. Immediately send a `task.finished` event with a `pass` result

This is easy and very quick to get started but it has two behaviours that should be known.

1. AppRunner is always assumed to finish immediately
1. AppRunner is always assumed to finish successfully

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/awsapprunner/1.0.0/assets/fire-and-forget-webhook.png)

# Fire and Wait Trigger App Runner

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/awsapprunner/1.0.0/assets/fire-and-wait-sequence.svg)

This is a more complex integration which requires modification of your AppRunner and the ability for it to send the `task.finished` event back to Keptn.

The concept is similar to the [AWS Lambda integration](https://artifacthub.io/packages/keptn/keptn-integrations/aws-lambda). A code example to send a finished event is available on [this page](https://artifacthub.io/packages/keptn/keptn-integrations/aws-lambda).

1. Webhook service listens for `task` event (usually a `task.triggered` event)
1. Webhook service sends a `task.started` event back to Keptn automatically
1. Webhook service triggers AppRunner
1. AppRunner completes some work. Optionally AppRunner can send `task.status.changed` events during execution to update Keptn of ongoing progress.
1. AppRunner crafts and sends back the `task.finished` event with a `Result`

In this integration style, AppRunner is responsible for sending the finished events back to Keptn which provides four benefits:

1. AppRunner can signal back to Keptn during execution using the `status.changed` event
1. Keptn knows the accurate timing of the AppRunner task and the sequence will pause until AppRunner is finished
1. Keptn knows the correct status of the AppRunner task - did it pass or fail?
1. AppRunner can pass custom data or metrics back to Keptn so subsequent tools can use the data

# AppRunner Triggers Keptn

This is an integration the opposite way around. Here, AppRunner is triggering a Keptn sequence.

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/awsapprunner/1.0.0/assets/app-runner-trigger-keptn-sequence.svg)


The AppRunner code needs to craft a `sequence.triggered` payload and `POST` it to the Keptn `/api/v1/event` endpoint.

```
POST https://myKeptn.com/api/v1/event
-H "x-token: <KeptnAPIToken>"
-H "content-type": "application/json"

Body:
{
  "specversion": "1.0",
  "contenttype": "application/json",
  "data": {
      "project": "<projectNameHere>",
      "service": "<serviceNameHere>",
      "stage": "<stageNameHere>"
  },
  "type": "sh.keptn.event.<stageNameHere>.<sequenceNameHere>.triggered",
  "source": "aws-app-runner"
}
```

## Need help?
[Keptn Slack](https://keptn.sh/community/#slack) is a great place for questions.