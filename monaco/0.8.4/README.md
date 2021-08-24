# Keptn Service for Dynatrace Monaco

This is a Sandbox Keptn Services that enables calling the Dynatrace Monaco (Monitoring as Code) toolset for individual Keptn Events

For more information on Dynatrace Monaco, visit the git repository https://github.com/dynatrace-oss/dynatrace-monitoring-as-code

## Installation

The *monaco-service* can be installed as a part of [Keptn's uniform](https://keptn.sh).

### Deploy in your Kubernetes cluster

To deploy the current version of the *monaco-service* in your Keptn Kubernetes cluster, apply the [`deploy/service.yaml`](deploy/service.yaml) file:

```console
kubectl apply -f deploy/service.yaml
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
kubectl delete -f deploy/service.yaml
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
```console
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

```console
zip -r monaco.zip directory_name
```

You can add the file to Keptn by using 
```console
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
For an example, please check [tagging.json](monaco/projects/monaco/auto-tag/tagging.json/)