# Keptn Microsoft Teams Webhook Integration

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/msteams/1.0.0/assets/1.png)

Configure MS Teams notifications from Keptn using the Keptn `webhook service` and the incoming Webhooks connector of Microsoft Teams

## Step 1: MS Teams Incoming Webhook Connector

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/msteams/1.0.0/assets/2.png)

Create a new `Incoming webhook connector` in Teams. Click on the channel and go to `Connectors`. Create an incoming webhook named `Keptn`.triggered

Download the Keptn logo from here: `https://github.com/keptn/keptn/blob/master/assets/keptn_logo.png` and upload it via the prompt.

Click `Create` and a webhook URL will be generated.

```
https://acmecorp.webhook.office.com/webhookb2/abcd1234-2345-4567-aaaa-aaaa1234bbbb@abcd1234-5432-4321-1111-abcd1234defg/IncomingWebhook/abcd1111222233334444aaaabbbbcccc/12334dd4-abcd-1234-abcd-1234abcd1234
```

## Step 2: Webhook Service Configuration

Create a new subscription for the Keptn webhook service.

- Set the URL to the webhook URL provided in step 1
- Add a new header: `Content-Type: application/json`
- Add a payload body below as a template

```
{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "000000",
  "summary": "Keptn Quality Gate Evaluation",
  "sections": [{
    "activityTitle": "Keptn Quality Gate Evaluation",
    "activityImage": "https://github.com/keptn/keptn/raw/master/assets/keptn_logo.png",
    "facts": [{
        "name": "Result",
        "value": "{{.data.evaluation.result}}"
      }, {
        "name": "Score",
        "value": "{{.data.evaluation.score}}%"
      }, {
        "name": "Project",
        "value": "{{.data.project}}"
      }, {
        "name": "Service",
        "value": "{{.data.service}}"
      }, {
        "name": "stage",
        "value": "{{.data.stage}}"
      }, {
        "name": "Date",
        "value": "{{.data.evaluation.timeStart}} - {{.data.evaluation.timeEnd}}"
      }],
    "markdown": true
    }],
  "potentialAction": [{
    "@type": "OpenUri",
    "name": "View Evaluation",
    "targets": [{
        "os": "default",
        "uri": "https://YourKeptn.com/bridge/evaluation/{{.shkeptncontext}}/{{.data.stage}}"
      }]
  }]
}
```

![](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/msteams/1.0.0/assets/3.png)
