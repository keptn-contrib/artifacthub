# PagerDuty Integration

[PagerDuty](https://support.pagerduty.com/docs/) is a project management and incident monitoring platform. This page describes how to integrate Keptn with PagerDuty.

![pd model](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/pagerduty/1.0.0/assets/pd2.png)

## Overview
The [keptn webhook service](https://github.com/keptn/keptn/tree/master/webhook-service) is documented on the [Webhook Integration](https://keptn.sh/docs/0.19.x/integrations/webhooks/) page, which comes "out of the box" with Keptn, will be used to listen for Keptn events and trigger webhooks into PagerDuty. In this way, new PagerDuty projects, tasks or anything else in PagerDuty are created in response to a [Keptn CloudEvent](https://keptn.sh/docs/0.19.x/reference/miscellaneous/events/).

Examples:
  - Create a new task each time a deployment occurs. Include the pass / fail status of the deployment
  - Create a new task each time a load test or evaluation is finished. Include the results and any output of the test / evaluation
  - Tag PagerDuty users in tasks to notify them that action is required

## Step 1: Gather PagerDuty Details
1. Navigate to our [Sign Up page](https://www.pagerduty.com/sign-up/) for a PagerDuty account, enter your Work Email and then click Get Started and complete the next steps.
1. Enter a Subdomain: PagerDuty accounts are accessible via a personalized subdomain. If your company name is EveryNine Inc., for example, you can set your account's subdomain to everynine.pagerduty.com, dev-keptnr.pagerduty.com, or anything else.
1. Select the Service Region where you would like us to [host your account](https://support.pagerduty.com/docs/service-regions) and click Create Account to create your account.
1. To create a service, you can follow the steps provided [here](https://support.pagerduty.com/docs/services-and-integrations#create-a-service) and to add an integration to your service, you can choose [Events API v2](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview) which is highly reliable asynchronous API service and note the integration key as `routing key` as given in the below snapshot.

![pd events](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/pagerduty/1.0.0/assets/pd3.png)

## Step 2: Keptn Webhook Setup
> This can be done [programmatically](https://keptn.sh/docs/0.19.x/integrations/webhooks/#configure-active-webhook-on-task-triggered-events) using `curl` request or via the Keptn Bridge

1. Navigate to a Keptn project and to go the Integrations screen
1. Click the webhook-service and setup the task subscription
1. Set the method as `POST`
1. Set the URL as `https://events.pagerduty.com/v2/enqueue`
1. Set the `Content-Type` header to `application/json`
1. Modify the payload below to your liking and use it as the `body` content

To know more about the request body, you can check out the details from [here](https://developer.pagerduty.com/api-reference/368ae3d938c9e-send-an-event-to-pager-duty).

```
{
  "payload": {
    "summary": "Keptn Evaluation: {{.data.result}}",
    "timestamp": "{{.time}}",
    "severity": "warning",
    "source": "http://X.Y.Z.X/bridge/project/myapp/",
    "component": "qa",
    "group": "prod-datapipe"
  },
  "routing_key": your-integration-key,
  "dedup_key": "srv01/qa",
  "event_action": "trigger",
  "client": "Keptn monitoring tool",
  "client_url": "http://X.Y.Z.X/bridge/project/myapp/"
}
```

That's it! Execute the sequence and PagerDuty service task /incidents will be automatically created.

![pd events](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/pagerduty/1.0.0/assets/pd1.png)