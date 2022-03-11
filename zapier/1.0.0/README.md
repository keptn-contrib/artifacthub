# Keptn Zapier Integration

## Usage: Zapier Responds to Keptn
  
Create a Zap that uses Webhooks by Zapier to run whatever Zap you want. Then configure the Keptn webhook service to listen for the event you wish to react on (eg. `mysequence.finished` event)
  
When the Keptn sequence (or task) has completed, Keptn will trigger a webhook into Zapier, and the Zap will execute.

## Usage: Zapier Trigger Keptn
Zapier can also trigger Keptn sequences. At the end of a Zap, place an outgoing Webhook which fires an event to the Keptn `/api/v1/event` endpoint.
Use a valid `.triggered` cloud event (see below) and Keptn will start your sequence.
 
```
curl -X POST https://example.com/api/v1/event
--header "x-token": "<KeptnAPIToken>"
{
  "data": {
    "project": "<KeptnProjectName>",
    "service": "<KeptnServiceName>",
    "stage": "<KeptnStageName>"
  },
  "source": "zapier",
  "specversion": "1.0",
  "type": "sh.keptn.event.<KeptnStageName>.<KeptnSequenceName>.triggered"
}
```
  
## Usage: Do Both
Of course it is possible to use Zapier on both inputs and outputs.

### Example: Send an Email, Trigger a Sequence, Receive Results back via Email
Create 2 zaps.

- The first Zap lets you email Zapier with a formatted email. It then parses the email for Keptn details and triggers a sequence (using the Keptn API webhook).
- The second Zap relies on the Keptn webhook service listening for whatever event you like, the zap takes that payload and emails it to you.
  
![keptn zapier integration](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/zapier/1.0.0/assets/2zaps.png)