# Cloud Custodian Integration

  [Cloud Custodian](https://cloudcustodian.io) is described as "Opensource Cloud Security, Governance, and Management". Cloud Custodian can be used as part of a Keptn sequence to enforce cloud policies across AWS, Azure and GCP.

  ## Usage Example

  The AWS "getting started" policy from Cloud Custodian's website ensures all EC2 instances **with** a tag of `Custodian` are stopped:

  ```
  policies:
  - name: my-first-policy
    resource: aws.ec2
    filters:
      - "tag:Custodian": present
    actions:
      - stop
  ```

  ## Prerequisite: Store AWS Credentials in Secret
  Create a secret to hold your AWS credentials.
  
  If running the job executor service on the control plane, use `keptn create secret`. If running the job executor service on a remote execution plane, store as a kubectl secret.

  Examples:

  ```
  keptn create secret aws-creds \
  --from-literal=AWS_ACCESS_KEY_ID=ASIA***** \
  --from-literal=AWS_SECRET_ACCESS_KEY=****** \
  --from-literal=AWS_SESSION_TOKEN=******** \
  --from-literal=AWS_DEFAULT_REGION=us-east-1
  ```

  or

  ```
  kubectl -n keptn create secret generic aws-creds \
  --from-literal=AWS_ACCESS_KEY_ID=ASIA***** \
  --from-literal=AWS_SECRET_ACCESS_KEY=****** \
  --from-literal=AWS_SESSION_TOKEN=******** \
  --from-literal=AWS_DEFAULT_REGION=us-east-1
  ```

  ## Invoke Cloud Custodian using Job Executor Service

  The [Job Executor Service](https://github.com/keptn-contrib/job-executor-service) can be invoked to execute this policy.

  1. Create a folder in the root of your stage branch called `files`
  2. Inside the `files` folder, create a file to hold the above policy (eg. `stop.tagged.ec2.instances.yaml`)
  3. Move back one directory to the root and create a `job/config.yaml` file for the Job Executor

  ```
  apiVersion: v2
  actions:
    - name: "Run Cloud Custodian Policy"
      events:
        - name: "sh.keptn.event.policy.triggered"
      tasks:
        - name: "Run Policies with CloudCustodian"
          files:
            - 'files'
          env:
            - name: aws-creds
              valueFrom: secret
          image: "cloudcustodian/c7n:0.9.15.0"
          args:
            - 'run'
            - '-s .'
            - '/keptn/files/stop.tagged.ec2.instances.yaml'
  ```