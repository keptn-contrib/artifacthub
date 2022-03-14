# NeoLoad Webhook Integration

This integration runs a load test on NeoLoad Web leveraging [Keptn's Webhooks](https://keptn.sh/docs/0.13.x/integrations/webhooks/).

This integration allows Performance engineers and developers to automatically trigger a load test on the application
when it is released to staging or other testing environments. This will save engineers time and increase confidence in the performance of their applications.

Below is an example NeoLoad Web Test Result overview pages as triggered by the Keptn webhook.
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/1.0.0/images/neoload-web-test-result.png)

## Prerequisites 

### Step 1: Create a Test in NeoLoad Web

See [NeoLoad documentation](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#40118.htm) for details on how to create a test.

### Step 2: Deploy resources

Ensure that enough resources attached to NeoLoad Web to successfully run the load test.
See [NeoLoad documentation](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#41350.htm) for details for configuring controller and load generator resource zones.

### Step 3: Collect Test and Workspace ID.

These IDs are needed later for the configuration of the Keptn webhook.

- The Test ID of the test can be found in the URL of the new test
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/1.0.0/images/test-id.png)
- The Workspace ID can be found in the URL of the "Settings" page
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/1.0.0/images/workspace-id.png)

### Step 4: Create or collect the NeoLoad Web Access token of a tester or admin user.

The access token is needed later for the configuration of the Keptn webhook.
See [Neoload documentation](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#24621.htm) for details on Access Tokens

Please be aware that the NeoLoad Web access token is sensitive data. If this data is known by other parties, they can use NeoLoad Web API to access all your tests and results.

### Step 5: Create Keptn Secret

To securely store your NeoLoad Web access token, a Keptn secret must be created.
To do this, select a project then click on **Uniform page** > **Secrets** and click the **Add Secret**.  On that form fill the following values:

* *Name:* `neoload-webhook`
* *Scope:* `keptn-webhook-service`
* *Key-value pairs*: Click the new key-value pair button and add these values:
  - *Key* = `accountToken`
  - *Value* = The NeoLoad Web account token from the previous section

The completed form should look as follows:
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/1.0.0/images/secret-configuration.png)

### (Optional) Validate you have Keptn Webhook Service deployed

Keptn Webhook Service was introduced with **Keptn 0.10.0** and is getting installed by default on the Control Plane. If you manually installed Keptn or upgraded manually,
please validate and ensure that your Keptn installation runs the Keptn `webhook-service`.

## Configure Keptn for NeoLoad Webhook
NeoLoad web supports [Keptn passive webhooks](https://www.dynatrace.com/support/help/how-to-use-dynatrace/cloud-automation/lifecycle-orchestration) where the
webhook subscription just listens for a task started or task finished event and then calls the NeoLoad API to run a performance test.
Once the NeoLoad webhook is triggered, NeoLoad does not need to send anything back to Keptn.  Instead, the Keptn sequence will just automatically continue.

You can incorporate NeoLoad webhooks into any Keptn project, but the example in this section assumes you have created a Keptn project called **demo**,
a stage called **performance**, a service called **demoservice**, and a sequence with a task called **trigger-neoload-test**.

### Step 1: Configure webhook

1. In a Keptn project, go to **Uniform page** > **Uniform**, select the webhook-service, and click the *Add subscription* button.
2. For the subscription section, fill in the following:
   * *Task*: `trigger-neoload-test`
   * *Task suffix*: `triggered`
3. For the webhook configuration section, fill in the following:
   * *Request Method*: POST
   * *URL*: The NeoLoad API endpoint with the workspace and test ID using this syntax `https://neoload-api.saas.neotys.com/v3/workspaces/<Your WorkspaceID>/tests/<Your TestID>/start?testResultName=<Your Test Result Name>&testResultDescription=<Your test result description>`
   * For example: `https://neoload-api.saas.neotys.com/v3/workspaces/5e3abde2e860a13ca619/tests/f61787dd-da45-44f0-9e0d-a76b4a0371e/start?testResultName=Demo-Test-Result&testResultDescription=stage-{{.data.stage}}`
   * Refer to the [NeoLoad Web API documentation](https://neoload-api.saas.neotys.com/explore/) for more details
   * Add a custom header with the following values:
     - *name*: accountToken
     - *value*: {{.secret.neoload-webhook.accountToken}}
   * The Custom Payload field can be left empty.

The completed form should look as follows:
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/1.0.0/images/webhook.png)

4. Click the Create subscription button to save and enable the webhook

### Step 2: Adjust webhook

A Keptn UI enhancement is coming, but for now you need to manually adjust the `webhook.yaml` simulate the task being run.
This will allow the *trigger-neoload-test* to start and finish automatically.
1. Open the project in your git upstream repo and adjust the `webhook/webhook.yaml` file in the `master` branch.
2. Find the `sh.keptn.event.trigger-neoload-test.triggered` entry and add a row with `sendFinished: true` between `type` and `requests`.
3. Commit your change

Below is an example webhook.yaml file as reference
```yaml
apiVersion: webhookconfig.keptn.sh/v1alpha1
kind: WebhookConfig
metadata:
  name: webhook-configuration
spec:
  webhooks:
    - type: sh.keptn.event.trigger-neoload-test.triggered
      sendFinished: true
      requests:
        - "curl --header 'accountToken:
          {{.env.secret_neoloadapitoken_accountToken}}' --request POST
          https://neoload-api.saas.neotys.com/v3/workspaces/5e3acde2e860a132744\
          ca916/tests/f61787dd-da45-44f0-9e0d-a7bf4a03701e/start?testResultName\
          =Demo-Test-Result&testResultDescription=stage-{{.data.stage}}"
      envFrom:
        - name: secret_neoloadapitoken_accountToken
          secretRef:
            name: neoload-api-token
            key: accountToken
      subscriptionID: 170def39-1234-1234-1234-5c89bd9b1aa3
```

### Step 3: Run sequence

With those steps done, Keptn will trigger a NeoLoad Action whenever a *trigger-neoload-test.finished* task event occurs. To test this example setup:
* Run the sequence using the using the [Keptn CLI](https://keptn.sh/docs/0.13.x/reference/cli/)
* Monitor the Keptn sequence progress in the Keptn Bridge sequence page
* Monitor the NeoLoad test execution within NeoLoad Web Test Result page.


## Feedback

If you have any feedback or additional examples please let us know within the [Tricentis support portal](https://feedback.tricentis.com). The best way is to either leave a comment on this Git repo, 
do a PR.
