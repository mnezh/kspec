# Kubernetes deployment validation framework

## Setup
With Python 3.9+ (might work in 3.8):

```shell
$ make setup
```

## Run tests
With default k8s context in `~/.kube/config` pointing to HAIC installation:

```shell
$ make test
```

The `test` target takes optional arguments:
* `K8S_CONTEXT` - name of k8s context in the `~/.kube/config`
* `ENV_CONFIG` - path to yaml file defining the environment (see [config/replicated-kots.yaml](config/replicated-kots.yaml))
* `MARKERS` - [pytest markers](https://docs.pytest.org/en/7.1.x/example/markers.html), like `"not keycloak"`

Examples:
* With non-default k8s context
```shell
$ make test K8S_CONTEXT=arn:aws:eks:us-west-2:524466471676:cluster/qa0331-aws-cluster
```
* With predefined environment and keycloak tests skipped
```shell
$ make test ENV_CONFIG=config/replicated-kots.yaml MARKERS="not keycloak"
```

## Sample results
```shell
tests/appstore/test_appstore.py:

Appstore namespace:

  Healthy namespace:
    ✓ Has healthy pod[server]

  Namespace pods with volumes:
    ✓ Pods has expected volumes[server appstore-conf]
    ✓ Pods has expected volumes[server kube-api-access]

  Namespace with tls secret:
    » Has tls secret
```

# Detailed Allure report
You need [allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) installed.

```shell
$ make allure
```
![Allure screenshot](docs/allure.png?raw=true "Allure screenshot")

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)