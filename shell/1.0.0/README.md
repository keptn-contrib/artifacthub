# Shell Script Execution

Execute any shell script with Keptn by using the [Job Executor Service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service)

For example:
```
apiVersion: v2
actions:
  - name: "Run alpine image to say hello world"
    events:
      - name: "sh.keptn.event.hello-world.triggered"
    tasks:
      - name: "Say Hello World"
        image: "alpine"
        cmd:
          - echo
        args:
          - 'Hello, world!'
```