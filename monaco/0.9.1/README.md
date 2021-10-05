# Keptn Service for Dynatrace Monaco

This is a Sandbox Keptn Services that enables calling the Dynatrace Monaco (Monitoring as Code) toolset for individual Keptn Events

For more information on Dynatrace Monaco, visit the git repository https://github.com/dynatrace-oss/dynatrace-monitoring-as-code

---

# monaco-service
![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-sandbox/monaco-service)
[![Go Report Card](https://goreportcard.com/badge/github.com/keptn-sandbox/monaco-service)](https://goreportcard.com/report/github.com/keptn-sandbox/monaco-service)

This implements a monaco-service for Keptn. If you want to learn more about Keptn visit us on [keptn.sh](https://keptn.sh)

## Compatibility Matrix

*Please fill in your versions accordingly*

|Authors | Keptn Version    | [monaco-service Docker Image](https://hub.docker.com/r/keptnsandbox/monaco-service/tags) | Comment |
|:----------------:|:----------------:|:----------------------------------------:|:----------------:|
|[@kristofre](https://github.com/kristofre)|       0.7.3      | keptnsandbox/monaco-service:0.1.0 | Initial release |
|[@grabnerandi](https://github.com/grabnerandi)|       0.7.3      | keptnsandbox/monaco-service:0.2.0 | Support for monaco folder structure |
|[@grabnerandi](https://github.com/grabnerandi)|       0.7.3      | keptnsandbox/monaco-service:0.2.1 | Fixes & Label Env Variable Support |
|[@grabnerandi](https://github.com/grabnerandi)|       0.8.0-0.8.3      | keptnsandbox/monaco-service:0.8.0 | Upgrade to support Keptn 0.8.0 |
|[@grabnerandi](https://github.com/grabnerandi)|       0.8.4      | keptnsandbox/monaco-service:0.8.4 | Upgrade to support Keptn 0.8.4 |
|[@grabnerandi](https://github.com/grabnerandi)|       0.9.1      | keptnsandbox/monaco-service:0.9.1 | Upgrade to support Keptn 0.9.1 |

## Installation

The *monaco-service* can be installed as a part of [Keptn's uniform](https://keptn.sh).

### Deploy in your Kubernetes cluster

To deploy the current version of the *monaco-service* in your Keptn Kubernetes cluster, apply the [`https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml`](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml) file:

```console
kubectl apply -f https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml
```

This should install the `monaco-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment monaco-service -o wide
kubectl -n keptn get pods -l run=monaco-service
```

### Up- or Downgrading

Adapt and use the following command in case you want to up- or downgrade your installed version (specified by the `$VERSION` placeholder):

```console
kubectl -n keptn set image deployment/monaco-service monaco-service=keptnsandbox/monaco-service:$VERSION --record
```

### Uninstall

To delete a deployed *monaco-service*, use the file `deploy/*.yaml` files from this repository and delete the Kubernetes resources:

```console
kubectl delete -f https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml
```

## Usage

The goal of the *monaco-service* is to allow the user to trigger Dynatrace Monaco as part of their keptn-driven releases. For more information about how Dynatrace Monaco works, please check the git repository README: https://github.com/dynatrace-oss/dynatrace-monitoring-as-code

It needs the following configured:

### Kubernetes secret for Dynatrace Environment

* A Kubernetes secret containing the values `DT_TENANT` and `DT_API_TOKEN` is needed. The `DT_API_TOKEN` should have the permission to **read** and **write configuration**
* The *monaco-service* looks by default for the following secrets: `dynatrace`, `dynatrace-credentials` and `dynatrace-credentials-$PROJECT`. If a different secret name can be configured by adding a resource `dynatrace\monaco.conf.yaml`. In this file you can specificy in the variable `dtCreds` the name of a secret containing the info.

### Option 1: Monaco projects folders

You can upload your monaco configuration on the service, stage or project level. If you do you have to follow the monaco folder structure starting with `projects` under the dynatrace subfolder.
The folder structure should therefore be the following:
```
+-- dynatrace // this is where the dynatrace related config goes in general
|   +-- projects // this folder name needs to be used
|       +-- projectName (this can be customized)
|           +-- configuration1 (check monaco documentation for the possible options)
|               +-  json and yaml files (check monaco documentation for the possible options)
|       +-- projectN
|           +-- json and yaml files

```

You can add these files to Keptn by using 
```
keptn add-resource --project=PROJECTNAME --service=SERVICENAME --stage=STAGENAME --resource=auto-tag/tagging.json --resourceUri=dynatrace/projects/keptnservice/auto-tag/tagging.json
keptn add-resource --project=PROJECTNAME --service=SERVICENAME --stage=STAGENAME --resource=auto-tag/tagging.yaml --resourceUri=dynatrace/projects/keptnservice/auto-tag/tagging.yaml
```

`stage` and `service` are optional. The monaco-service will automatically download all files under the dynatrace/projects directory first on the `service` level, then on `stage` level and last on `project` level.

### Option 2: A ZIP archive containing the projects

Now - this is the same as Option 1 - but - instead of having each file separate in Keptn's configuration repo you can also just zip it up and upload the zipped projects directoy to the dynatrace subfolder
The folder structure should be the following:
```
+-- projects // this folder name needs to be used
|   +-- projectName (this can be customized)
|       +-- configuration1 (check monaco documentation for the possible options)
|           +-  json and yaml files (check monaco documentation for the possible options)
|   +-- projectN
|       +-- json and yaml files

```
**Note:** the archive has to be of type `zip`. Using the `zip` command on linux, it can be created as follows:

```
zip -r monaco.zip directory_name
```

You can add the file to Keptn by using 
```
keptn add-resource --project=PROJECTNAME --service=SERVICENAME --stage=STAGENAME --resource=monaco.zip --resourceUri=dynatrace/monaco.zip
```

`stage` and `service` are optional. The monaco-service will automatically look for this file first on the `service` level, then on `stage` level and last on `project` level.

### Specifying which monaco projects to process

If not specified, the *monaco-service* looks for a monaco project with the name of the keptn project. So if your keptn project name is `sockshop`, then you would need the following structure in the `monaco.zip` file:
```
+-- projects 
|   +-- sockshop 
|       +-- auto-tag (an example) 
|           +-  json and yaml files
```

If you want to overwrite that behaviour, it is possible to specify that in the `dynatrace\monaco.conf.yaml` file by adding them as follows:
```
projects:
  - monaco
  - sockshop
  - infrastructure
```

All the projects that you want to process can be added. So for the above, you would need the following structure: 
```
+-- projects 
|   +-- infrastructure 
|       +-- synthetic-location 
|           +-  json and yaml files
|   +-- monaco 
|       +-- auto-tag
|           +-  json and yaml files
|   +-- sockshop 
|       +-- management-zone 
|           +-  json and yaml files
```

### Using Keptn metadata inside monaco files

The monaco-service automatically maps the following Keptn information as environment variables:
* Keptn project name as env var `KEPTN_PROJECT`
* Keptn stage name as env var `KEPTN_STAGE`
* Keptn service name as env var `KEPTN_SERVICE`

They can then be used inside monaco files as follows: `{{ Env.KEPTN_PROJECT }}`
For an example, please check [tagging.json](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/monaco/projects/monaco/auto-tag/tagging.json/)




## Development

This is an open source project, so I welcome any contributions to make it even better!

### Where to start

If you don't care about the details, your first entrypoint is [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/eventhandlers.go](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/eventhandlers.go). Within this file 
 you can add implementation for pre-defined Keptn Cloud events.
 
To better understand Keptn CloudEvents, please look at the [Keptn Spec](https://github.com/keptn/spec).
 
If you want to get more insights, please look into [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/main.go](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/main.go), [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/deploy/service.yaml),
 consult the [Keptn docs](https://keptn.sh/docs/) as well as existing [Keptn Core](https://github.com/keptn/keptn) and
 [Keptn Contrib](https://github.com/keptn-contrib/) services.

### Build yourself

* Build the binary: `go build -ldflags '-linkmode=external' -v -o monaco-service`
* Run tests: `go test -race -v ./...`
* Build the docker image: `docker build . -t keptnsandbox/monaco-service:dev` (Note: Ensure that you use the correct DockerHub account/organization)
* Run the docker image locally: `docker run --rm -it -p 8080:8080 keptnsandbox/monaco-service:dev`
* Push the docker image to DockerHub: `docker push keptnsandbox/monaco-service:dev` (Note: Ensure that you use the correct DockerHub account/organization)
* Deploy the service using `kubectl`: `kubectl apply -f deploy/`
* Delete/undeploy the service using `kubectl`: `kubectl delete -f deploy/`
* Watch the deployment using `kubectl`: `kubectl -n keptn get deployment monaco-service -o wide`
* Get logs using `kubectl`: `kubectl -n keptn logs deployment/monaco-service -f`
* Watch the deployed pods using `kubectl`: `kubectl -n keptn get pods -l run=monaco-service`
* Deploy the service using [Skaffold](https://skaffold.dev/): `skaffold run --default-repo=your-docker-registry --tail` (Note: Replace `your-docker-registry` with your DockerHub username; also make sure to adapt the image name in [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/skaffold.yaml](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/skaffold.yaml))


### Testing Cloud Events

We have dummy cloud-events in the form of [RFC 2616](https://ietf.org/rfc/rfc2616.txt) requests in the [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/test-events/](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/test-events/) directory. These can be easily executed using third party plugins such as the [Huachao Mao REST Client in VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).


## License

Please find more information in the [https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/LICENSE](https://raw.githubusercontent.com/keptn-sandbox/monaco-service/release-0.9.1/LICENSE) file.
