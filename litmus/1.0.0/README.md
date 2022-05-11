# Litmus Chaos Keptn Integration

![](https://raw.githubusercontent.com/keptn-sandbox/litmus-service/master/assets/litmus-keptn.png)

Use Litmus Chaos to perform chaos tests on your applications triggered by Keptn using the LitmusChaos framework.

This integration uses the [Job Executor Service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service) before continuing, ensure you have installed and configured the Job Executor Service.

The instructions below assume you will configure the [Job Executor Service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service) to listen for `sh.keptn.event.chaos.triggered` events. Feel free to change `chaos` to whatever your shipyard task is called. If you do so, also modify the given `job/config.yaml` file below.

## Use Litmus Chaos with Job Executor Service

1. Change to the relevant stage branch in the Keptn Git upstream repo eg. `dev`
1. Create two folders: `job` and `locust`
1. Create a file: `job/config.yaml` with the contents below
1. Upload your locust specific files inside the `locust` folder


### **job/config.yaml**
```
apiVersion: v2
actions:
  - name: "Print files"
    events:
      - name: "sh.keptn.event.chaos.triggered"
    tasks:
      - name: "Run locust tests"
        files:
          - locust/
        image: "locustio/locust"
        cmd:
          - locust
        args:
          - '--config'
          - /keptn/locust/locust.conf
          - '-f'
          - /keptn/locust/basic.py
          - '--host'
          - $(HOST)
```

## Explanation

When you installed the [job executor service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service), you configured it to listen for one (or more) Keptn `task.triggered` events. If you followed the instructions above, it will be `sh.keptn.event.chaos.triggered`.

The config file above tells the [job executor service](https://artifacthub.io/packages/keptn/keptn-integrations/job-executor-service) to:

1. Copy all of the files from the `locust` folder in the Git repo into the container under the `/keptn/` directory. So `/locust/file.py` in Git becomes `/keptn/locust/file.py` inside the container.
1. Create a container from the `locustio/locust` image
1. Run the container with the given `cmd` and `args`

If the container exits successfully (a zero exit code) the task is finished with a `pass`. Should the container fail, the `task.finished` keptn event has a result of `fail`.