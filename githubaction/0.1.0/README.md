# GitHub Actions via Keptn Webhooks

This integration shows how to invoke GitHub Action workflows leveraging [Keptn's Webhook Service](https://keptn.sh/docs/0.10.x/integrations/webhooks/).  With a GitHub actions integration, you can call existing GitHub workflows from Keptn sequences. 

[WATCH THIS VIDEO TUTORIAL](https://www.youtube.com) to see this in action!

# Prerequisites

## Step 1: Configure GitHub

1. GitHub Access Token

    A GitHub personal access token (PAT) is required to pass within the Keptn webhook authorization header in order for the GitHub API to authenticate the request. Follow these instructions in the [GitHub docs](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) to create your token and be sure that you have given the token access to the `repo` [scope](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps).

1. GitHub repo with a GitHub Action

    The GitHub repository must have at least one action workflow. If you are not familiar with GitHub, we recommend you review the [GitHub getting started documentation](https://docs.github.com/en/actions/learn-github-actions).

1. GitHub Action configured to support repository dispatch

    Use the GitHub API to trigger a webhook event called [repository_dispatch](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#repository_dispatch) that will start a GitHub action workflow. 
  
    To use repository dispatches, configure your GitHub workflow with the `repository_dispatch` trigger and provide a dispatch name that will match to the value. Within the Keptn webhook payload that is sent to the GitHub action API request, the `event_type` attribute is how GitHub matches the request to the GitHub workflow to run.  
    
    Below is an example with a repository dispatch with the event type name of `silent`.

    ```
    name: webhook silent example
    on:
      repository_dispatch:
        types: 
          - silent
    ```

## Step 2: Store GitHub token as a Keptn secret

To secure the GitHub Access Token, a Keptn secret must be created.  To do this, go to the Keptn project  `Uniform page > Secret` and click the `Add Secret` button.  On that form fill the following values:
  * **Name**: Name such as `github-secret` 
  * **Scope**: `keptn-webhook-service` 
  * **Key-value pairs**:  Click the `new key-value pair` button and add these values:
    * **Key** = Name such as `GITHUBTOKEN`
    * **Value** = The GitHub Access Token from the step from previous section 

The completed form should look as follows:

<img src="images/createsecret.png" width="50%" height="50%">

## Step 3: Create Keptn project

The examples use case in the next sections below assume you have created a Keptn project with a [shipyard file](https://keptn.sh/docs/0.10.x/manage/shipyard/) as follows:

```
apiVersion: spec.keptn.sh/0.2.2
kind: "Shipyard"
metadata:
  name: "demo-webhook"
spec:
  stages:
    - name: "production"
      sequences:
      - name: "mysequence"
        tasks: 
        - name: "mytask-interactive"
```

# GitHub integration Webhook options

There are two use cases for Keptn webhooks:

1. **Silent** - The webhook subscription listens for status events, `started` or `finished`, and calls the GitHub Action API to invoke the GitHub workflow. GitHub does not need to send anything back to Keptn and the Keptn sequence will just continue to process.
1. **Interactive** -  The webhook subscription listens for`triggered` events, calls the GitHub Action API to invoke the GitHub workflow. Once it does the  Keptn sequence will wait until the GitHub workflow to send back a `finished` event.

## Use Case 1: Silent webhook

This example shows a GitHub workflow that is triggered when a Keptn task called `myTask` sends its `finished` Keptn event within the `dev` or `staging` stage of the Keptn project. 

1. In a Keptn project, go to `Uniform page > Uniform`, select the `webhook-service`, and click the `Add subscription` button.
1. For the subscription section, fill in the following:
    * **Task**: `evaluation`
    * **Task suffix**: `finished`
1. For the webhook configuration section, fill in the following:
    * **Request method**: `POST`
    * **URL**: The API endpoint of the repo: `https://api.github.com/repos/[ORG-NAME]/[REPO-NAME]/dispatches` 
    * Add a custom header with the following values:
      * **Name** = `Authorization`
      * **Value** = `token {{.secret.github-secret.GITHUBTOKEN}}`
    * Custom Payload must contain the following JSON attributes:
      * The `event_type` entry is a required attribute with a value that matches one of the event types defined in the GitHub actions workflow file. If the `event_type` value does not match any types defined in any GitHub actions, then nothing happens and the webhook request passes silently. 
      * The `client_payload` attribute is a JSON payload with extra information about the webhook event that your action or workflow may use
      * Below is an an custom payload with the `event_type` equal to `silent`:

      ``` 
      {
        "event_type": "silent",
        "client_payload": {
          "type": "{{.type}}",
          "project": "{{.data.project}}",
          "service": "{{.data.service}}",
          "stage": "{{.data.stage}}",
          "shkeptncontext": "{{.shkeptncontext}}",
          "id": "{{id}}"
        }
      }
      ```
    * The completed form should look as follows:
    
      <img src="images/silent-subscription.png" width="50%" height="50%">

    * Refer to the [GitHub documentation](https://docs.github.com/en/rest/reference/repos#create-a-repository-dispatch-event) for more information on the repository dispatch event.

1. Click the `Create subscription` button to save and enable the webhook for your GitHub Action integration.

1. Below is an example GitHub action script with the `repository_dispatch` set to match the value `silent` that is passed in the  `client_payload` values sent by the Keptn webhook.  This example just displays the values from the `client_payload`.

    ```
    name: webhook silent example
    on:
      repository_dispatch:
        types: 
          - silent
    jobs:
      test:
        name: Test
        runs-on: ubuntu-latest
        steps:
        - name: show client_payload
          run: |
            echo "Received silent webhook, just displaying data"
            echo "type": "${{ github.event.client_payload.type }}"
            echo "shkeptncontext": "${{ github.event.client_payload.shkeptncontext }}"
    ```

1. With those steps done, Keptn will trigger a GitHub Action whenever an `evaluation.finished` event occurs.  To test this example setup:

  * Run the `keptn trigger evaluation` event using the [Keptn CLI](https://keptn.sh/docs/0.10.x/reference/cli/)
  * Monitor the Keptn sequence progress in the Keptn Bridge sequence page
  * Monitor the GitHub workflow execution on the GitHub actions page.

## Use Case 2: Interactive webhook 

The previous use case just triggers a GitHub action workflow. This use case will have the Keptn sequence wait until the GitHub workflow to send back a `finished` event.

1. In a Keptn project, go to `Uniform page > Uniform`, select the `webhook-service`, and click the `Add subscription` button.
1. For the subscription section, fill in the following:
    * **Task**: `mytask-interactive`
    * **Task suffix**: `triggered`
1. For the webhook configuration section, fill in the following:
    * **Request method**: `POST`
    * **URL**: The API endpoint of the repo: `https://api.github.com/repos/[ORG-NAME]/[REPO-NAME]/dispatches` 
    * Add a custom header with the following values:
      * **Name** = `Authorization`
      * **Value** = `token {{.secret.github-secret.GITHUBTOKEN}}`
    * Custom Payload must contain the following JSON attributes:
      * The `event_type` entry is a required attribute with a value that matches one of the event types defined in the GitHub actions workflow file. If the `event_type` value does not match any types defined in any GitHub actions, then nothing happens and the webhook request passes silently. 
      * The `client_payload` attribute is a JSON payload with extra information about the webhook event that your action or workflow may use
      * Below is an an custom payload with the `event_type` equal to `interactive`:

      ``` 
      {
        "event_type": "interactive",
        "client_payload": {
          "type": "{{.type}}",
          "project": "{{.data.project}}",
          "service": "{{.data.service}}",
          "stage": "{{.data.stage}}",
          "data": "{{.data.custom}}",
          "shkeptncontext": "{{.shkeptncontext}}",
          "id": "{{.id}}"
        }
      }
      ```

    * The completed form should look as follows:

      <img src="images/interactive-subscription.png" width="50%" height="50%">

    * Refer to the [GitHub documentation](https://docs.github.com/en/rest/reference/repos#create-a-repository-dispatch-event) for more information on the repository dispatch event.

1. Click the `Create subscription` button to save and enable the webhook for your GitHub Action integration.

1. For a `interactive` webhook, one must also adjust the webhook configuration file to NOT auto-respond with a finished event.  In upcoming releases, this will be configurable from the Bridge UI.  To perform this task, refer to the [Keptn documentation](https://keptn.sh/docs/0.10.x/integrations/webhooks/#configure-webhook-to-not-auto-respond-with-a-finished-event).

1. In order for the GitHub workflow to call the Keptn API, create two [GitHub repository action secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) with the Keptn API URL and Keptn API Token.

    * Go to GitHub repos `Settings > Secret` and click add these two secrets:
      * `KEPTN_BASE_URL` = Use the base URL for your environment such as: `https://[YOUR-TENANT].cloudautomation.dynatrace.com` for the secret value.
      * `KEPTN_API_TOKEN` = From the Bridge UI, click on the profile icon on the top right. From the profile popup window, copy the API token and use that for the secret value
    * The completed secrets should look as follows:

      <img src="images/github-secret.png" width="50%" height="50%">

1. Below is an example GitHib action script with the `repository_dispatch` set to match the value `interactive` that is passed in the  `client_payload` values sent by the Keptn webhook.  This example extracts the values from the passed in `client_payload` to construct and send back the Keptn task `finished` event.

    ```
    name: webhook interactive example
    on:
      repository_dispatch:
        types: 
          - interactive
    jobs:
      test:
        name: Keptn Interactive Example
        runs-on: ubuntu-latest
        steps:
        - name: do some work
          run: echo "Performing some workflow logic"
        - name: send keptn finished event
          run: |
            echo "Received interactive webhook, will send back Keptn finished event"
            json=$(cat <<-END
                {
                  "data": {
                    "project":"${{ github.event.client_payload.project }}",
                    "stage": "${{ github.event.client_payload.stage}}",
                    "service": "${{ github.event.client_payload.service}}",
                    "status": "succeeded",
                    "result": "pass"
                  },
                  "source": "github",
                  "specversion": "1.0",
                  "type": "sh.keptn.event.mytask-interactive.finished",
                  "shkeptncontext": "${{ github.event.client_payload.shkeptncontext }}",
                  "triggeredid": "${{ github.event.client_payload.id }}"
                }
            END
            )
            echo "json=$json"
            curl -X POST "${{ secrets.KEPTN_API_URL }}/v1/event" -H "Content-Type: application/json" -H "accept: application/json" -H "x-token: ${{ secrets.KEPTN_API_TOKEN }}" -d "$json"
    ```

1. With those steps done, Keptn will trigger a GitHub Action whenever an `mysequence.triggered` event occurs.  To test this example setup:

  * Create a file called `triggered-event.json` with the following contents:
      ```
      {
        "type": "sh.keptn.event.production.mysequence.triggered",
        "specversion":"1.0",
        "source":"cas-quickstart",
        "data":{
            "project":"demo",
            "stage":"production",
            "service":"casdemoapp",
        }
      }
      ```

  * Run this [Keptn CLI](https://keptn.sh/docs/0.10.x/reference/cli/) command `keptn send event --file triggered-event.json` 
  * Monitor the Keptn sequence progress in the Keptn Bridge sequence page
  * Monitor the GitHub workflow execution on the GitHub actions page.

# Cleanup

To delete a webhook, click on the trash can icon next to the subscription. Note that deleting a webhook is permanent and cannot be reversed. Once deleted, Keptn will no longer send requests to the endpoint.

# Feedback

If you have any feedback or additional examples please let us know. Best way is to either leave a comment on this Git repo, do a PR or join our conversation in the [Keptn Slack Channel](https://slack.keptn.sh)
