# README

Use this branch to deploy `jira-service` if you're running Keptn `0.8.3`.

```
git clone --branch release-0.8.3 https://github.com/keptn-sandbox/jira-service
```

# jira-service
![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-sandbox/jira-service)
[![Go Report Card](https://goreportcard.com/badge/github.com/keptn-sandbox/jira-service)](https://goreportcard.com/report/github.com/keptn-sandbox/jira-service)

This implements a jira-service for Keptn. If you want to learn more about Keptn visit us on [keptn.sh](https://keptn.sh)

## Compatibility Matrix

| Keptn Version    | [jira-service Docker Image](https://hub.docker.com/r/keptnsandbox/jira-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.8.5      | keptnsandbox/jira-service:0.8.5 |
|       0.8.4      | keptnsandbox/jira-service:0.8.4 |
|       0.8.3      | keptnsandbox/jira-service:0.8.3 |
|       0.8.2      | keptnsandbox/jira-service:0.8.2 |
|       0.8.1      | keptnsandbox/jira-service:0.8.1 |
|       0.8.0      | keptnsandbox/jira-service:0.8.0 |

# Gather JIRA Information
You'll need the following information to use this plugin.

1. JIRA Base URL (without trailing slash) eg. `https://abc123.atlassian.net`
1. JIRA Username eg. `joe.smith@example.com`
1. JIRA ID for Ticket Reporter (see below for how to retrieve)
1. JIRA ID for Ticket Assignee (can be same as reporter ID)
1. JIRA API Token ([generate one here](https://id.atlassian.com/manage/api-tokens))
1. JIRA Project Key. Take this from the URL. Eg. `PROJ` is the project code for `https://abc123.atlassian.net/projects/PROJ/issues`
1. JIRA Issue Type eg. Task, Bug, Epic etc. Defaults to `Task`.
1. Keptn base URL (eg. `https://example.com` or however you've exposed Keptn)
1. Keptn bridge URL (eg. `https://example.com/bridge`)

## Retrieve User IDs (IMPORTANT)
JIRA now require the User ID for both the ticket reporter and the assignee.

Retrieve these by clicking your profile icon (top right) then go to profile and grab your ID from the end of the URL:

![image](https://user-images.githubusercontent.com/13639658/113224119-0a615000-92ce-11eb-9abd-693efa2ac612.png)

# Save JIRA Details as k8s Secret
Paste your values into the command below (replacing `***`) and save the JIRA details into a secret called `jira-details` in the `keptn` namespace.

```console
kubectl -n keptn create secret generic jira-details \
--from-literal="keptn-domain=https://1.2.3.4" \
--from-literal="keptn-bridge-url=https://1.2.3.4/bridge" \
--from-literal="jira-base-url=***" \
--from-literal="jira-username=***" \
--from-literal="jira-reporter-user-id=***" \
--from-literal="jira-assignee-user-id=***" \
--from-literal="jira-api-token=***" \
--from-literal="jira-project-key=***" \
--from-literal="jira-issue-type=Task" \
--from-literal="jira-create-ticket-for-problems=true" \
--from-literal="jira-create-ticket-for-evaluations=true"
```

Expected output:

```
secret/jira-details created
```

## Installation

The *jira-service* can be installed as a part of [Keptn's uniform](https://keptn.sh).

Do not deploy from `master` branch. Please switch to the release branch that matches your Keptn version.

### Deploy in your Kubernetes cluster

To deploy the current version of the *jira-service* in your Keptn Kubernetes cluster, apply the [`https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/deploy/service.yaml`](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/deploy/service.yaml) file:

```console
kubectl apply -f deploy/service.yaml
```

This should install the `jira-service` together with a Keptn `distributor` into the `keptn` namespace, which you can verify using

```console
kubectl -n keptn get deployment jira-service -o wide
kubectl -n keptn get pods -l run=jira-service
```

### Logs
Retrieve container logs with:

```
kubectl logs -n keptn -l run=jira-service -c jira-service
```

Retrieve distributor logs with:
```
kubectl logs -n keptn -l run=jira-service -c distributor
```

### Up- or Downgrading

Adapt and use the following command in case you want to up- or downgrade your installed version (specified by the `$VERSION` placeholder):

```console
kubectl -n keptn set image deployment/jira-service jira-service=keptnsandbox/jira-service:$VERSION --record
```

### Uninstall

To delete a deployed *jira-service*, use the file `deploy/*.yaml` files from this repository and delete the Kubernetes resources:

```console
kubectl delete -f deploy/service.yaml
```

## Development

Development can be conducted using any GoLang compatible IDE/editor (e.g., Jetbrains GoLand, VSCode with Go plugins).

It is recommended to make use of branches as follows:

* `master` contains the latest potentially unstable version
* `release-*` contains a stable version of the service (e.g., `release-0.1.0` contains version 0.1.0)
* create a new branch for any changes that you are working on, e.g., `feature/my-cool-stuff` or `bug/overflow`
* once ready, create a pull request from that branch back to the `master` branch

When writing code, it is recommended to follow the coding style suggested by the [Golang community](https://github.com/golang/go/wiki/CodeReviewComments).

### Where to start

If you don't care about the details, your first entrypoint is [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/eventhandlers.go](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/eventhandlers.go). Within this file 
 you can add implementation for pre-defined Keptn Cloud events.
 
To better understand all variants of Keptn CloudEvents, please look at the [Keptn Spec](https://github.com/keptn/spec).
 
If you want to get more insights into processing those CloudEvents or even defining your own CloudEvents in code, please 
 look into [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/main.go](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/main.go) (specifically `processKeptnCloudEvent`), [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/deploy/service.yaml](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/deploy/service.yaml),
 consult the [Keptn docs](https://keptn.sh/docs/) as well as existing [Keptn Core](https://github.com/keptn/keptn) and
 [Keptn Contrib](https://github.com/keptn-contrib/) services.

### Common tasks

* Build the binary: `go build -ldflags '-linkmode=external' -v -o jira-service`
* Run tests: `go test -race -v ./...`
* Build the docker image: `docker build . -t keptnsandbox/jira-service:dev` (Note: Ensure that you use the correct DockerHub account/organization)
* Run the docker image locally: `docker run --rm -it -p 8080:8080 keptnsandbox/jira-service:dev`
* Push the docker image to DockerHub: `docker push keptnsandbox/jira-service:dev` (Note: Ensure that you use the correct DockerHub account/organization)
* Deploy the service using `kubectl`: `kubectl apply -f deploy/`
* Delete/undeploy the service using `kubectl`: `kubectl delete -f deploy/`
* Watch the deployment using `kubectl`: `kubectl -n keptn get deployment jira-service -o wide`
* Get logs using `kubectl`: `kubectl -n keptn logs deployment/jira-service -f`
* Watch the deployed pods using `kubectl`: `kubectl -n keptn get pods -l run=jira-service`
* Deploy the service using [Skaffold](https://skaffold.dev/): `skaffold run --default-repo=your-docker-registry --tail` (Note: Replace `your-docker-registry` with your DockerHub username)


### Testing Cloud Events

We have dummy cloud-events in the form of [RFC 2616](https://ietf.org/rfc/rfc2616.txt) requests in the [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/test-events/](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/test-events/) directory. These can be easily executed using third party plugins such as the [Huachao Mao REST Client in VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

## Automation

### GitHub Actions: Automated Pull Request Review

This repo uses [reviewdog](https://github.com/reviewdog/reviewdog) for automated reviews of Pull Requests. 

You can find the details in [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.github/workflows/reviewdog.yml](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.github/workflows/reviewdog.yml).

### GitHub Actions: Unit Tests

This repo has automated unit tests for pull requests. 

You can find the details in [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.github/workflows/tests.yml](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.github/workflows/tests.yml).

### GH Actions/Workflow: Build Docker Images

This repo uses GH Actions and Workflows to test the code and automatically build docker images.

Docker Images are automatically pushed based on the configuration done in [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.ci_env](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/.ci_env) and the two [GitHub Secrets](https://github.com/keptn-sandbox/jira-service/settings/secrets/actions)
* `REGISTRY_USER` - your DockerHub username
* `REGISTRY_PASSWORD` - a DockerHub [access token](https://hub.docker.com/settings/security) (alternatively, your DockerHub password)

## How to release a new version of this service

It is assumed that the current development takes place in the master branch (either via Pull Requests or directly).

To make use of the built-in automation using GH Actions for releasing a new version of this service, you should

* branch away from master to a branch called `release-x.y.z` (where `x.y.z` is your version),
* write release notes in the [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/releasenotes/](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/releasenotes/) folder,
* check the output of GH Actions builds for the release branch, 
* verify that your image was built and pushed to DockerHub with the right tags,
* update the image tags in [deploy/service.yaml], and
* test your service against a working Keptn installation.

If any problems occur, fix them in the release branch and test them again.

Once you have confirmed that everything works and your version is ready to go, you should

* create a new release on the release branch using the [GitHub releases page](https://github.com/keptn-sandbox/jira-service/releases), and
* merge any changes from the release branch back to the master branch.

## License

Please find more information in the [https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/LICENSE](https://raw.githubusercontent.com/keptn-sandbox/jira-service/release-0.8.3/LICENSE) file.
