# Infracost Integration with Keptn

[![Keptn Infracost Quality Gate Example](https://img.youtube.com/vi/L8AWjCAHv-4/0.jpg)](https://www.youtube.com/watch?v=L8AWjCAHv-4 "Keptn Infracost Quality Gate Example")

![infracost running in keptn](https://raw.githubusercontent.com/keptn-contrib/artifacthub/main/infracost/1.0.0/assets/infracost-keptn.png)

This integration uses the [job executor service](https://github.com/keptn-contrib/job-executor-service).

## Prerequisites

You will need:

- An infracost API token (see [get an API token](https://www.infracost.io/docs/#2-get-api-key))
- To install the job executor service (see below)
- (optional) Install an SLI provider (eg. Dynatrace, Prometheus, DataDog etc.)

## How it Works
The Job executor service is configured to listen for a `sh.keptn.event.{task}.triggered` event (if following the example files, this is `sh.keptn.event.checkcost.triggered`).

The job executor:
1. Creates a new Kubernetes job
2. Copies in the Terrafrom plan.json file from the Keptn git repo at `/files/plan.json` into the container at `/keptn/files/plan.json`.
3. Reads the `infracost-details` secret and sets the `INFRACOST_API_TOKEN` environment variable
4. Sends an `sh.keptn.event.checkcost.started` event to Keptn
5. Runs `infracost breakdown --path /keptn/files/plan.json --format table`
6. Sends an `sh.keptn.event.checkcost.finished` event to Keptn, with the tabular output

## Install Job Executor Service
Follow the [Job executor service install instructions](https://github.com/keptn-contrib/job-executor-service#quickstart) to install on a cluster (either local to Keptn control plane components or on a different cluster).

Ensure the Job Executor Service is installed listening for the `sh.keptn.event.taskname.triggered` event that corresponds to your Shipyard file (see below).

Below, the task is `checkcost` so JES should listen for `sh.keptn.event.checkcost.triggered`.

Create a Kubernetes secret in the same namespace.

- The name (`infracost-details`) can be changed but must match what you use in `job/config.yaml` (see later).
- The key `INFRACOST_API_KEY` **cannot** be changed as infracost relies on exactly this as an environment variable.

```
kubectl -n YOUR_NAMESPACE create secret generic infracost-details \
--from-literal=INFRACOST_API_KEY=YOUR_INFRACOST_API_KEY
```

## Add Necessary Files
In your Git upstream, add the following files to your stage branch (eg. `dev`). These should be placed inside the service folder.

For example: `service1/job/config.yaml` on the `dev` branch.

## Example Shipyard

```
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "infracost-shipyard"
spec:
  stages:
    - name: "dev"
      sequences:
        - name: "demosequence"
          tasks:
            - name: "checkcost"
```

## Example Job Executor Config File
```
apiVersion: v2
actions:
  - name: "Run infracost"
    events:
      - name: "sh.keptn.event.checkcost.triggered"
    tasks:
      - name: "Execute Infracost"
        workingDir: "/keptn"
        files:
          - /files/plan.json
        image: "infracost/infracost:ci-0.10.8"
        cmd:
          - "infracost"
        args:
          - 'breakdown'
          - '--path'
          - '/keptn/files/plan.json'
          - '--format'
          - 'table'
        env:
          - name: infracost-details
            valueFrom: secret
```

## Example Terraform plan.json File
```
{
	"format_version": "1.0",
	"terraform_version": "1.1.4",
	"planned_values": {
		"root_module": {
			"resources": [{
				"address": "aws_instance.web_app",
				"mode": "managed",
				"type": "aws_instance",
				"name": "web_app",
				"provider_name": "registry.terraform.io/hashicorp/aws",
				"schema_version": 1,
				"values": {
					"ami": "ami-674cbc1e",
					"credit_specification": [],
					"ebs_block_device": [{
						"delete_on_termination": true,
						"device_name": "my_data",
						"iops": 800,
						"tags": null,
						"volume_size": 500,
						"volume_type": "io1"
					}],
					"get_password_data": false,
					"hibernation": null,
					"iam_instance_profile": null,
					"instance_type": "m5.4xlarge",
					"launch_template": [],
					"root_block_device": [{
						"delete_on_termination": true,
						"tags": null,
						"volume_size": 50
					}],
					"source_dest_check": true,
					"tags": null,
					"timeouts": null,
					"user_data_replace_on_change": false,
					"volume_tags": null
				},
				"sensitive_values": {
					"capacity_reservation_specification": [],
					"credit_specification": [],
					"ebs_block_device": [{}],
					"enclave_options": [],
					"ephemeral_block_device": [],
					"ipv6_addresses": [],
					"launch_template": [],
					"maintenance_options": [],
					"metadata_options": [],
					"network_interface": [],
					"private_dns_name_options": [],
					"root_block_device": [{}],
					"secondary_private_ips": [],
					"security_groups": [],
					"tags_all": {},
					"vpc_security_group_ids": []
				}
			}, {
				"address": "aws_lambda_function.hello_world",
				"mode": "managed",
				"type": "aws_lambda_function",
				"name": "hello_world",
				"provider_name": "registry.terraform.io/hashicorp/aws",
				"schema_version": 0,
				"values": {
					"code_signing_config_arn": null,
					"dead_letter_config": [],
					"description": null,
					"environment": [],
					"file_system_config": [],
					"filename": null,
					"function_name": "hello_world",
					"handler": "exports.test",
					"image_config": [],
					"image_uri": null,
					"kms_key_arn": null,
					"layers": null,
					"memory_size": 1024,
					"package_type": "Zip",
					"publish": false,
					"reserved_concurrent_executions": -1,
					"role": "arn:aws:lambda:us-east-1:account-id:resource-id",
					"runtime": "nodejs12.x",
					"s3_bucket": null,
					"s3_key": null,
					"s3_object_version": null,
					"tags": null,
					"timeout": 3,
					"timeouts": null,
					"vpc_config": []
				},
				"sensitive_values": {
					"architectures": [],
					"dead_letter_config": [],
					"environment": [],
					"ephemeral_storage": [],
					"file_system_config": [],
					"image_config": [],
					"tags_all": {},
					"tracing_config": [],
					"vpc_config": []
				}
			}]
		}
	},
	"resource_changes": [{
		"address": "aws_instance.web_app",
		"mode": "managed",
		"type": "aws_instance",
		"name": "web_app",
		"provider_name": "registry.terraform.io/hashicorp/aws",
		"change": {
			"actions": ["create"],
			"before": null,
			"after": {
				"ami": "ami-674cbc1e",
				"credit_specification": [],
				"ebs_block_device": [{
					"delete_on_termination": true,
					"device_name": "my_data",
					"iops": 800,
					"tags": null,
					"volume_size": 500,
					"volume_type": "io1"
				}],
				"get_password_data": false,
				"hibernation": null,
				"iam_instance_profile": null,
				"instance_type": "m5.4xlarge",
				"launch_template": [],
				"root_block_device": [{
					"delete_on_termination": true,
					"tags": null,
					"volume_size": 50
				}],
				"source_dest_check": true,
				"tags": null,
				"timeouts": null,
				"user_data_replace_on_change": false,
				"volume_tags": null
			},
			"after_unknown": {
				"arn": true,
				"associate_public_ip_address": true,
				"availability_zone": true,
				"capacity_reservation_specification": true,
				"cpu_core_count": true,
				"cpu_threads_per_core": true,
				"credit_specification": [],
				"disable_api_stop": true,
				"disable_api_termination": true,
				"ebs_block_device": [{
					"encrypted": true,
					"kms_key_id": true,
					"snapshot_id": true,
					"throughput": true,
					"volume_id": true
				}],
				"ebs_optimized": true,
				"enclave_options": true,
				"ephemeral_block_device": true,
				"host_id": true,
				"id": true,
				"instance_initiated_shutdown_behavior": true,
				"instance_state": true,
				"ipv6_address_count": true,
				"ipv6_addresses": true,
				"key_name": true,
				"launch_template": [],
				"maintenance_options": true,
				"metadata_options": true,
				"monitoring": true,
				"network_interface": true,
				"outpost_arn": true,
				"password_data": true,
				"placement_group": true,
				"placement_partition_number": true,
				"primary_network_interface_id": true,
				"private_dns": true,
				"private_dns_name_options": true,
				"private_ip": true,
				"public_dns": true,
				"public_ip": true,
				"root_block_device": [{
					"device_name": true,
					"encrypted": true,
					"iops": true,
					"kms_key_id": true,
					"throughput": true,
					"volume_id": true,
					"volume_type": true
				}],
				"secondary_private_ips": true,
				"security_groups": true,
				"subnet_id": true,
				"tags_all": true,
				"tenancy": true,
				"user_data": true,
				"user_data_base64": true,
				"vpc_security_group_ids": true
			},
			"before_sensitive": false,
			"after_sensitive": {
				"capacity_reservation_specification": [],
				"credit_specification": [],
				"ebs_block_device": [{}],
				"enclave_options": [],
				"ephemeral_block_device": [],
				"ipv6_addresses": [],
				"launch_template": [],
				"maintenance_options": [],
				"metadata_options": [],
				"network_interface": [],
				"private_dns_name_options": [],
				"root_block_device": [{}],
				"secondary_private_ips": [],
				"security_groups": [],
				"tags_all": {},
				"vpc_security_group_ids": []
			}
		}
	}, {
		"address": "aws_lambda_function.hello_world",
		"mode": "managed",
		"type": "aws_lambda_function",
		"name": "hello_world",
		"provider_name": "registry.terraform.io/hashicorp/aws",
		"change": {
			"actions": ["create"],
			"before": null,
			"after": {
				"code_signing_config_arn": null,
				"dead_letter_config": [],
				"description": null,
				"environment": [],
				"file_system_config": [],
				"filename": null,
				"function_name": "hello_world",
				"handler": "exports.test",
				"image_config": [],
				"image_uri": null,
				"kms_key_arn": null,
				"layers": null,
				"memory_size": 1024,
				"package_type": "Zip",
				"publish": false,
				"reserved_concurrent_executions": -1,
				"role": "arn:aws:lambda:us-east-1:account-id:resource-id",
				"runtime": "nodejs12.x",
				"s3_bucket": null,
				"s3_key": null,
				"s3_object_version": null,
				"tags": null,
				"timeout": 3,
				"timeouts": null,
				"vpc_config": []
			},
			"after_unknown": {
				"architectures": true,
				"arn": true,
				"dead_letter_config": [],
				"environment": [],
				"ephemeral_storage": true,
				"file_system_config": [],
				"id": true,
				"image_config": [],
				"invoke_arn": true,
				"last_modified": true,
				"qualified_arn": true,
				"signing_job_arn": true,
				"signing_profile_version_arn": true,
				"source_code_hash": true,
				"source_code_size": true,
				"tags_all": true,
				"tracing_config": true,
				"version": true,
				"vpc_config": []
			},
			"before_sensitive": false,
			"after_sensitive": {
				"architectures": [],
				"dead_letter_config": [],
				"environment": [],
				"ephemeral_storage": [],
				"file_system_config": [],
				"image_config": [],
				"tags_all": {},
				"tracing_config": [],
				"vpc_config": []
			}
		}
	}],
	"configuration": {
		"provider_config": {
			"aws": {
				"name": "aws",
				"expressions": {
					"access_key": {
						"constant_value": "mock_access_key"
					},
					"region": {
						"constant_value": "us-east-1"
					},
					"secret_key": {
						"constant_value": "mock_secret_key"
					},
					"skip_credentials_validation": {
						"constant_value": true
					},
					"skip_requesting_account_id": {
						"constant_value": true
					}
				}
			}
		},
		"root_module": {
			"resources": [{
				"address": "aws_instance.web_app",
				"mode": "managed",
				"type": "aws_instance",
				"name": "web_app",
				"provider_config_key": "aws",
				"expressions": {
					"ami": {
						"constant_value": "ami-674cbc1e"
					},
					"ebs_block_device": [{
						"device_name": {
							"constant_value": "my_data"
						},
						"iops": {
							"constant_value": 800
						},
						"volume_size": {
							"constant_value": 500
						},
						"volume_type": {
							"constant_value": "io1"
						}
					}],
					"instance_type": {
						"constant_value": "m5.4xlarge"
					},
					"root_block_device": [{
						"volume_size": {
							"constant_value": 50
						}
					}]
				},
				"schema_version": 1
			}, {
				"address": "aws_lambda_function.hello_world",
				"mode": "managed",
				"type": "aws_lambda_function",
				"name": "hello_world",
				"provider_config_key": "aws",
				"expressions": {
					"function_name": {
						"constant_value": "hello_world"
					},
					"handler": {
						"constant_value": "exports.test"
					},
					"memory_size": {
						"constant_value": 1024
					},
					"role": {
						"constant_value": "arn:aws:lambda:us-east-1:account-id:resource-id"
					},
					"runtime": {
						"constant_value": "nodejs12.x"
					}
				},
				"schema_version": 0
			}]
		}
	}
}
```

## Infracost as a Quality Gate (Pushing Metrics)

Most users will wish to export the Infracost metric into a metric storage system like Dynatrace or Prometheus. From there, the metrics can be retrieved later and used in a Keptn quality gate evaluation.

To do so, ensure you have an SLI provider service installed (eg. Dynatrace, Prometheus etc.).

Then instead of directly running the Infracost container, run a Python script / shell script or some other "Wrapper" which will trigger Infracost and then push the metrics when Infracost has finished running.

Sample code for this for both Dynatrace and Prometheus is available on the [metric exporter instructions page](https://artifacthub.io/packages/keptn/keptn-integrations/metric-exporter).