# Jira Keptn Service

This implements a jira-service for Keptn. If you want to learn more about Keptn visit us on keptn.sh

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

To deploy the current version of the *jira-service* in your Keptn Kubernetes cluster, apply the [`deploy/service.yaml`](deploy/service.yaml) file:

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

```console
kubectl logs -n keptn -l run=jira-service -c jira-service
```

Retrieve distributor logs with:
```console
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