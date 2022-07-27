# Akamas Webhook Integration

This integration enables developers, performance engineers, DevOps, and SREs to get their applications automatically optimized in terms of performance, resilience, and cost efficiency (according to any defined application-specific goal), when these applications are released into staging or other testing environments. The integration of Akamas with Keptn ensures that services provide the highest quality at the lowest possible cost.

## Prerequisites 

1. Install Akamas (make sure you have a valid license).
2. Port 6000 must be open on the Akamas server. 
3. Install the Akamas pre-built container on the Akamas server. This container will act as a bi-directional bridge between Akamas Studies and Keptn webhooks. Make sure host and port 6000 is publicly reachable on the Akamas server. Port 6000 is the predefined port and if you need to use a different host, or certificate, then please contact Akamas support.

    <details>
    <summary>How to install the Akamas container</summary>

    - Make an application directory such as /usr/local/keptn
    - In the application directory, download the files below.
      ```bash
      curl https://akamas.s3.us-east-2.amazonaws.com/integrations/keptn/docker-compose.yml -o docker-compose.yml
      curl https://akamas.s3.us-east-2.amazonaws.com/integrations/keptn/env.templ -o .env
      ```
    - Edit the `docker-compose.yml` file by specifying the certificate folder and corresponding files in order to expose the integration API called by Keptn webhook via HTTPS. This is the same folder specified when enabling HTTPS on Akamas. The predefined names for the certificates are `akamas.pem` and `akamas.key`.
    - Edit the `.env` file by replacing the values of the `KEPTN_URL` and `KEPTN_TOKEN` variables with your own values. 
    - Start the container.
      ```bash
      docker-compose up -d
      ```
    </details>

## Installation

### Step 1: Akamas

Set up the desired optimization study on the Akamas side and save the Study ID for later use. 

### Step 2: Subscribe to a Keptn event to invoke an Akamas Study

To configure Akamas integration with Keptn, follow the steps below.

1. Create a Keptn project with a shipyard file, and a task (for example, `optimize`) to get Akamas optimization triggered in the desired stage (for example, `staging`).
2. On the Keptn bridge, go to **Uniform** > Secret menu and select **Add Secret**.
3. Enter the following values:

    - **Name** - enter `akamas` 
    - **Scope** -  enter `keptn-webhook-service`
    - **Key** - enter `pwd`
    - **Value** - enter a base64 encoded `user:password` combination. For example, if user is `akamas` and password is `testpassword`, then the combined `user:password` `akamas:testpassword` gets encoded into `YWthbWFzOnRlc3RwYXNzd29yZA==`. To easily encode your password, see [Encode to Base64 format](https://www.base64encode.org/).
4. Select **Add secret**.
5. Create a webhook subscription to the `optimize` task. 
    - **Task suffix**, enter `triggered`.
    - **Request method**, enter `POST`
    - **URL**, enter `https://<akamas-url>:6000/v1/study-run` (make sure to replace the placeholder `<akamas-url>` with your actual Akamas URL).
    - In **Custom header**, enter two entries
      - For **Name**, enter `Authorization`. For **Value**, enter `Basic {{.secret.akamas.pwd}}`.
      - For **Name**, enter `Content-Type`, and for **Value**, enter `application/json`.
    - In **Custom payload**, enter the following. Make sure to replace `<study-id>` with the actual study ID value
        ```json
        {
            "study-id": "<study-id>",
            "project": "{{.data.project}}",
            "stage": "{{.data.stage}}",
            "service": "{{.data.service}}",
            "type": "{{.type}}",
            "shkeptncontext": "{{.shkeptncontext}}",
            "triggeredid": "{{.id}}"
        }
        ```
    - For **Send finished event** , select `by webhook receiver`.

## Run a sequence

Keptn calls Akamas whenever the defined task in the sequence is triggered.

1. When the task associated with the Akamas optimization in the sequence is executed, Keptn triggers the corresponding webhook service.
2. The webhook service launches the Akamas optimization, which is executed on the Akamas side.
3. Once the Akamas optimization is over, the finished event returning the result of the Akamas optimization is sent to Keptn.
 
You can get the sequence involving the Akamas task triggered by Keptn either by using the Keptn CLI or via UI. 

In the CLI:
1. Create a file called `triggered-event.json` with the following contents:
    ```json
    {
    "type": "sh.keptn.event.mystage.mysequence.triggered",
    "specversion":"1.0",
    "source":"manual-trigger",
    "data": {
      "project":"myproject",
      "stage":"mystage",
      "service":"myservice"
     }
    }
    ```
2. Run the command below.
    ```bash
    keptn send event --file triggered-event.json
    ```
    After sending the event, you can
    - Monitor the sequence progress on the Keptn sequence page of the project.
    - Monitor the Akamas study progress.
 
The following is an example of the structure of the event returned (in case of a optimization done at the JVM level):
 
```json
{
  "data": {
    "optimize": {
      "jvm": {
        "jvm_gcType": "G1",
        "jvm_maxHeapFreeRatio": 86,
        "jvm_maxHeapSize": 280,
        "jvm_maxTenuringThreshold": 4,
        "jvm_newSize": 268,
        "jvm_survivorRatio": 76
      }
    },
    …
  },
  …
}
```

## Clean up

To uninstall the Akamas-Keptn integration, follow the steps below.
 
### In Keptn

- Delete the webhook-service subscription.
- Remove the corresponding tasks from the sequences.
- Delete the Akamas secret.

### In Akamas

Remove the Akamas container.
```bash
docker-compose down
```