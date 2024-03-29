> This integration is for Keptn v1. It is no longer supported.
>
> Users are advised to use Keptn instead: https://keptn.sh

# Use AWS Lambda with Keptn

  There are two ways AWS Lambda can be used with keptn/kind:
  
  1. Run Lambda functions in response to Keptn tasks
  1. Trigger Keptn sequences from Lambda
  
  ## Execute Lambda from Keptn
  Executing Lambda functions in response to Keptn events allows a truly serverless workflow / paradigm.

  It is simple:
  
  1. Have the Keptn webhook trigger your lambda function

  Keptn needs a `task.finished` event so it knows the task has been actioned so EITHER:
  1. Instruct the webhook service to send the `task.finished` event automatically (returns immediately so will not accurately time lamda execution time) OR
  1. Craft a `task.finished` event in Lambda and send from your function (enables accurate Lambda execution time tracking in Keptn & ability to send data back to Keptn)
  
  First, subscribe the webhook-service to a `task.triggered` event. Set the endpoint as your Lambda URL.

  Set the body of the payload as:

  ```
  {
    "project": "{{.data.project}}",
    "service": "{{.data.service}}",
    "stage": "{{.data.stage}}",
    "type": "{{.type}}",
    "shkeptncontext": "{{.shkeptncontext}}",
    "triggeredid": "{{.id}}"
  }
  ```

  If you want the webhook-service to send the finished event automatically, pick `send finished event: automatically` or set `sendFinished: true` in the `webhook.yaml` file.

  If you want to accurately time and send data back to Keptn from Lambda, craft your own finished event.

  ## Crafted Finished Event (Python Example)

  ```
  import json
  import urllib3

  #
  # Assumes an incoming payload body of:
  # {
  #   "project": "{{.data.project}}",
  #   "service": "{{.data.service}}",
  #   "stage": "{{.data.stage}}",
  #   "type": "{{.type}}",
  #   "shkeptncontext": "{{.shkeptncontext}}",
  #   "triggeredid": "{{.id}}"
  # }
  #

  def lambda_handler(event, context):
    
    # Grab details from incoming webhook payload
    keptn_url = "https://myKeptn.com/api/v1/event"
    body = json.loads(event['body'])
    triggered_id = body['triggeredid']
    type = body['type'] # sh.keptn.event.sometask.started
    keptn_context = body['shkeptncontext']
    keptn_project = body['project']
    keptn_service = body['service']
    keptn_stage = body['stage']
    
    # create .finished type from .started string
    # transform sh.keptn.event.sometask.started to sh.keptn.event.sometask.finished
    task_index = type.rfind('.')
    finished_event_type = f"{type[:task_index]}.finished"
    
    headers = {
        "x-token": "abc12345",
        "content-type": "application/json"
    }
    
    data =  {
          "data": {
            "labels": { 
                "run_by": "aws_lambda"
            },
            "project": keptn_project,
            "service": keptn_service,
            "stage": keptn_stage
          },
          "source": "aws_lambda",
          "specversion": "1.0",
          "triggeredid": triggered_id,
          "shkeptncontext": keptn_context,
          "type": finished_event_type,
          "shkeptnspecversion": "0.2.3"
    }
    
    # Send finished event to Keptn
    http = urllib3.PoolManager()
    response = http.request(method="POST", headers=headers, url=keptn_url, body=json.dumps(data))
    
    return {
        'statusCode': 200,
        'body': ''
    }
  ```
  
  ## Trigger Keptn Sequences from Lambda
  This requires nothing more than an API call to the Keptn `/api/v1/event` endpoint.

  ### curl Example

  The curl would be (where the sequence name is `sequence1`):

  ```
  curl -X POST https://myKeptn.com/api/v1/event \
  -H x-token: abc12345 \
  -H content-type: application/json \
  --data '{
          "data": {
            "labels": {
              "run_by": "aws_lambda"
            },
            "project": "project1",
            "service": "service1",
            "stage": "stage1"
          },
          "source": "aws_lambda",
          "specversion": "1.0",
          "type": "sh.keptn.event.stage1.sequence1.triggered",
          "shkeptnspecversion": "0.2.3"
        }'
  ```

  ### Python Function Example

  The keptn library referenced below is found [here](https://github.com/agardnerIT/keptn_python_trigger).

  ```
  import json
  import urllib3
  from keptn import Keptn

  def lambda_handler(event, context):
    
    KEPTN_ENDPOINT = "https://myKeptn.com" # no trailing slash, /api/v1/event is autoamtically added by library code
    KEPTN_API_TOKEN = "*************"
    KEPTN_PROJECT = "project1"
    KEPTN_SERVICE = "service1"
    KEPTN_STAGE = "stage1"
    KEPTN_SEQUENCE_NAME = "sequence1"
    
    k1 = Keptn(url=KEPTN_ENDPOINT, api_token=KEPTN_API_TOKEN)
    k1.set_details(project=KEPTN_PROJECT, service=KEPTN_SERVICE, stage=KEPTN_STAGE)
    
    # Add your own custom data here
    # This is optional but if used, project, service and stage MUST stay
    data = {
        "labels": {
          "foo": "bar"
        },
        "project": KEPTN_PROJECT,
        "service": KEPTN_SERVICE,
        "stage": KEPTN_STAGE
    }
    
    #response = k1.trigger_sequence(sequence=KEPTN_SEQUENCE_NAME, from_source="aws_lambda")
    # OR with custom data block
    response = k1.trigger_sequence(sequence=KEPTN_SEQUENCE_NAME, from_source="aws_lambda", data_block=data)
    
    print(response.status)
    
    return {
        'statusCode': r.status,
        'body': r.data
    }
  ```