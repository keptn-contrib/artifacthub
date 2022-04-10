# Locust Job-Executor Integration

This integration shows you how to run performance tests using [Locust](https://locust.io/) and the [Keptn Job-Executor-Service](https://github.com/keptn-contrib/job-executor-service).

## Installation

Before running the integration, the job executor service needs to be installed. Please follow the [Job-Executor documentation](https://github.com/keptn-contrib/job-executor-service) for the installation process.

## Configure Locust using the Job-Executor-Service

### Step 1: Add the Job-Executor configuration file

The following configuration will allow you to run the tests inside [`locust/basic.py`](https://github.com/keptn-sandbox/locust-service/blob/main/test-data/basic.py) using the Job-Executor-Service whenever a test event is triggered.

locust.yaml:
```yaml
apiVersion: v2
actions:
  - name: "Run tests using locust"
    events:
      - name: "sh.keptn.event.test.triggered"
    tasks:
      - name: "Run locust"
        files:
          - locust/basic.py
          - locust/locust.conf

        image: "locustio/locust"
        cmd: ["locust"]
        args: ["--config", "/keptn/locust/locust.conf", "-f", "/keptn/locust/basic.py", "--host", "http://$(KEPTN_SERVICE).$(KEPTN_PROJECT)-$(KEPTN_STAGE)", "--only-summary"]
```

To add Locust to your service add the [`locust/basic.py`](https://github.com/keptn-sandbox/locust-service/blob/main/test-data/basic.py), [`locust/locust.conf`](https://github.com/keptn-sandbox/locust-service/blob/main/test-data/locust.conf) and `locust.yaml` files using the [`add-resource`](https://keptn.sh/docs/0.14.x/reference/cli/commands/keptn_add-resource/) command:

```
keptn add-resource --project=sockshop --service=carts --stage=dev --resource=./locust/basic.py
keptn add-resource --project=sockshop --service=carts --stage=dev --resource=./locust/locust.conf
keptn add-resource --project=sockshop --service=carts --stage=dev --resource=locust.yaml --resourceUri=job/config.yaml
```

Now the Job-Executor-Service will execute the Locust performance tests whenever you trigger a delivery, e.g., `keptn trigger delivery --project=sockshop --service=carts --image=docker.io/keptnexamples/carts --tag=0.13.1`

## Feedback

If you have any feedback or additional examples, please let us know. The best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh).