# Keptn Locust Service

This service provides a way to performance test on your application triggered by [Keptn](https://keptn.sh) using the [Locust](https://locust.io/) performance testing tool.

## Keptn CloudEvents

This service reacts on the following Keptn CloudEvents (see [deploy/service.yaml](deploy/service.yaml)):
* `sh.keptn.event.test.triggered` -> start locust performance tests
* `sh.keptn.event.test.finished` -> clean up resources and print results

## Installation -  Deploy in your Kubernetes cluster

To deploy the current version of the *locust-service* in your Keptn Kubernetes cluster, run

```console
kubectl apply -f https://raw.githubusercontent.com/keptn-sandbox/locust-service/release-0.1.5/deploy/service.yaml -n keptn
```

This will install the `locust-service` into the `keptn` namespace, which you can verify using:

```console
kubectl -n keptn get deployment locust-service -o wide
kubectl -n keptn get pods -l run=locust-service
```

## Usage

The `locust-service` expects locust test files in the project specific Keptn repo. It expects those files to be available in the `locust` subfolder for a service in the stage you want to execute tests.

Here is an example on how to upload the `locustfile.py` test file via the Keptn CLI to the dev stage of project sockshop for the service carts:

```console
keptn add-resource --project=sockshop --stage=dev --service=carts --resource=locustfile.py --resourceUri=locust/locustfile.py
```

### Defaults

If the user does not provide a specific configuration file (see next section) the `locust-service` will search for `locust/locustfile.py` in the specific Keptn repo and try to execute it. If the file does not exist the tests will be skipped.

### Providing a config file

A `locust.conf.yaml` file can be added for more complex configurations like multiple test files for different stages. It is also possible to provide a [locust config file](https://docs.locust.io/en/stable/configuration.html#configuration-file) to further customize the tests. If no configuration file is specified the `locust-service` will proceed with the default setting. 

```yaml
---
spec_version: '0.1.0'
workloads:
  - teststrategy: functional
    script: /locust/basic.py
    conf: /locust/locust.conf
  - teststrategy: performance_light
    script: /locust/basic.py
    conf: /locust/locust.conf
  - teststrategy: functional-light
    script: /locust/basic.py
```

The configuration file can be added to the repo using the `keptn add-resource` command:

```console
keptn add-resource --project=sockshop --service=carts --stage=dev --resource=locust.conf.yaml --resourceUri=locust/locust.conf.yaml
```

The contents of `locust.conf.yaml` should be used as described in the following:
- If a "script" is given, it has to be used in the execution of the locust test.
- If "script" is not given, we can assume that the script is part of the "config" file that is referenced.
- If a "conf" is given, it should be used in the execution of the locust test.
- If "conf" is not given, the "script" will be executed with default setting.
- If both "script" and "conf" are missing, the integration skips the tests and indicate this in the result that is sent back to Keptn.

Examples for both the `locust.conf.yaml` and the [locust config file](https://docs.locust.io/en/stable/configuration.html#configuration-file) can be found in the [test-data/](test-data) directory.

### Use kubernetes secrets as environment variables in the locust tests

The `locust-service` injects kubernetes secrets from its namespace with a matching name (`locust-<project>-<stage>-<service>`) as environment variables for the test execution. Secrets can be created with `kubectl`:

```console
kubectl -n keptn create secret generic locust-sockshop-dev-carts --from-literal=API_TOKEN=1234abcd --from-literal=PASSWORD=keptn
```

Now for tests in the project `sockshop`, stage `dev`, service `carts` the secrets will be available as environment variables in the locust tests:

```
os.environ['API_TOKEN']
os.environ['PASSWORD']
```

## Uninstall -  Delete from your Kubernetes cluster

To delete the locust-service, delete using the [`deploy/service.yaml`](deploy/service.yaml) file:

```console
kubectl delete -f deploy/service.yaml
```