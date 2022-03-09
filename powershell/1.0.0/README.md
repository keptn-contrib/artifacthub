# PowerShell Integration

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