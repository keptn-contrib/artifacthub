# PowerShell Integration

## Trigger a Keptn Sequence

Craft an HTTPS POST to trigger a Keptn sequence:

```
$headers = @{
  "x-token"="<YourKeptnAPIToken>"
  "Content-Type"="application/json"
}
$body = @'
{
  "type": "sh.keptn.event.<YourEnvironment>.<YourSequenceName>.triggered",
  "contenttype": "application/json",
  "source": "powershell-trigger",
  "data" : {
    "project": "<YourKeptnProject>",
    "service": "<YourKeptnService>",
    "stage": "<YourKeptnStage>",
    "labels": {
      "run_by": "<YourName>",
      ... etc.
    }
  },
  "specversion": "1.0"
}
'@
Invoke-RestMethod `
-Uri https://<YourKeptn>/api/v1/event `
-Method POST `
-Headers $headers `
-Body $body
```

This will trigger a sequence and return a Keptn context ID. This is the unique sequence ID for this run.

Then poll the `/api/mongodb-datastore/event/type/*` endpoint until a sequence `.finished` event matching the Keptn context ID is found.

```
curl -X GET "https://<YourKeptn.com>/api/mongodb-datastore/event/type/sh.keptn.event.<YourStage>.<YourSequence>.finished?filter=shkeptncontext:<YourKeptnContextID>&limit=1" \
-H "accept: application/json" \
-H "x-token: <Your-Keptn-API-Token>"
```

## Run Powershell as a Keptn Task

Run any Powershell command with Keptn and the [Job Executor Service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service)

For example:
```
apiVersion: v2
actions:
  - name: "Run alpine image to say hello world"
    events:
      - name: "sh.keptn.event.hello-world.triggered"
    tasks:
      - name: "Say Hello World"
        image: "mcr.microsoft.com/powershell:latest"
        cmd:
          - 'pwsh'
        args:
          - '-Command'
          - 'Write-Host Hello, World from PowerShell!'
```