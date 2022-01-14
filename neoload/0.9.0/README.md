# NeoLoad Webhook Integration

This integration shows you how to run a load test on NeoLoad Web leveraging [Keptn's Webhook capabilities](https://keptn.sh/docs/0.11.x/integrations/webhooks/).
This integration allows Performance testers and Developers to automatically trigger a load test on the application 
when it is released on staging/QA environment. This will save time to testers and increase confidence in the performance's application.

Here is a quick overview of a NeoLoad Test Result started by Keptn (the Test Result name and description can be customized):
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/0.9.0/images/neoload-web-test-result.png)

## Prerequisites 

### Step 1: Create a Test in NeoLoad Web

In NeoLoad Web, please follow the [NeoLoad Web documentation](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#40118.htm) to create a test.

### Step 2: Note Ids and access token

Keep these NeoLoad Web datas, they will be used later to configure the Keptn Webhook.

- Test ID: The ID of the test can be found in the URL
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/0.9.0/images/test-id.png)
- Workspace ID: The ID of the workspace where the test belongs can be found in the URL of the "Settings" page
![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/0.9.0/images/workspace-id.png)
- Account token of a tester or admin user. See [documentation of user profile](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#24621.htm).
Please be aware that the NeoLoad Web access token is sensitive data. If this data is known by other parties, 
they can use NeoLoad Web API to access all your tests and results. We will store this token as Keptn secret to keep it hidden.

### Step 3: Deploy resources

Deploy enough resources attached to NeoLoad Web to successfully run the load test. See [Documentation on how to associate a Controller Agent with a Zone](https://www.neotys.com/documents/doc/nlweb/latest/en/html/#41350.htm).

### (Optional) Validate you have Keptn Webhook Service deployed

Keptn Webhook Service was introduced with **Keptn 0.10.0** and is getting installed by default on the Control Plane. IFfyou manually installed Keptn or upgraded manually, please validate and ensure that your Keptn installation runs the Keptn `webhook-service`.

## Configure Keptn for NeoLoad Webhook

### Step 1: Create Keptn Secret for NeoLoad

To secure the sensitive data of your NeoLoad Web access token, a secret needs to be created:

* In Keptn, select a project then click on **Uniform page** > **Secrets** and click the **Add Secret**
* Then create a new secret with the following values:

  * *Name:* `neoload-webhook`
  * *Scope:* `keptn-webhook-service`

* And the following two key-value pairs:
```
accountToken: XXXXXXXXXXXXXXXXXXXXXXXX
```

For reference, here is a screenshot of that secret:

![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/0.9.0/images/secret-configuration.png)

### Step 2: Subscribe to a Keptn event to start NeoLoad Web test

To create a webhook integration, a subscription needs to be created:

* In Keptn, navigate to **Uniform page** -> **Uniform** and there select the **webhook-service**
* Click the **Add subscription** button, to create a new event subscription on the currently selected project.

**Example: Deployment Finished - Start a load test**

This is an example for sending a deployment finished event.

* In the *Create subscription* form section, fill out the following fields:
  * *Task:* `deployment`
  * *Task suffix:* `triggered`

* In the *Webhook configuration* form section fill out the following:
  * *Request Method*: POST
  * *URL*: `https://neoload-api.saas.neotys.com/v3/workspaces/<Your WorkspaceID>/tests/<Your TestID>/start?testResultName=Demo-test-result&testResultDescription=stage-{{.data.stage}}`
  * *Add a header*:
    - *name*: accountToken
    - *value*: {{.secret.neoload-webhook.accountToken}}

* Finally, click **Create subscription** to save and enable the webhook for your Slack integration.

* Here is a screenshot for your reference:
  ![](https://raw.githubusercontent.com/keptn-sandbox/artifacthub/main/neoload/0.9.0/images/deployment-finished-subscription.png)

* Update the webhook configuration on the git repository of the project to add the property `sendFinished: true`. The file `webhook/webhook.yaml` will look like:
```yaml
apiVersion: webhookconfig.keptn.sh/v1alpha1
kind: WebhookConfig
metadata:
  name: webhook-configuration
spec:
  webhooks:
    - type: sh.keptn.event.deployment.triggered
      sendFinished: true
      requests:
        - "curl --header 'accountToken: {{.env.secret_neoload-webhook_AccountToken}}'
          --request POST
          https://neoload-api.saas.neotys.com/v3/workspaces/5e3acde2e860a132744\
          ca916/tests/f61787dd-da45-44f0-9e0d-a7bf4a03701e/start?testResultName\
          =Demo-test-result&testResultDescription=stage-{{.data.stage}}"
      envFrom:
        - name: secret_neoload-webhook_AccountToken
          secretRef:
            name: neoload-webhook
            key: AccountToken
      subscriptionID: 170def39-1234-1234-1234-5c89bd9b1aa3
```


## Feedback

If you have any feedback or additional examples please let us know. The best way is to either leave a comment on this Git repo, 
do a PR.
