# How to contribute

## Setting up development environment
With Python 3.9+:

```shell
$ make setup
```

## Adding tests for the new namespace

* Add a pytest marker to [pyproject.toml](pyproject.toml)

```toml
markers = [
    "appstore: needs appstore namespace",
    "mynamespace: needs mynamespace namespace",
```

* Create a directory in [tests/](tests)

```shell
$ mkdir -p tests/kubernetes/mynamespace
```

* Create `tests/kubernetes/mynamespace/namespace.yaml` for your namespace

```yaml
name: mynamespace
pods:
  pod-name-suffix1:
    volumes:
      - should-have-this-volume
      - volume-name-is-regex.*
  pod-name-suffix2:
secrets:
  namespace-secret1:
  - it_has_this_data_key
  - and_some_other
  - they_key_value_should_not_be_empty
```

* Create `tests/kubernetes/mynamespace/test_mynamespace.py` for your namespace

```python
from k8spec import like, mark
from k8spec.traits import (
    healthy_namespace,
    namespace_pods_with_volumes,
    namespace_with_tls_secret,
    namespace_yaml,
)

 # all tests in module will have mynamespace mark, for pytest mark filters
pytestmark = mark("mynamespace")


@like( # your test could check for some of the predefined shared behaviors:
    namespace_yaml(__file__), # load namespace definition from yaml config
    healthy_namespace, # optional: your namespace has all expected pods in healthy state
    namespace_with_tls_secret, # optional: has expected certificate as TLS secret on Azure
    namespace_pods_with_volumes, # optional: all pods have expected volumes
)
def describe_appstore_namespace():
    pass
```

* Optionally add custom checks for your namespace:

```python
from k8satisfying import Namespace
from k8spec import rx
...
@like(
    namespace_yaml(__file__),
    healthy_namespace,
    namespace_with_tls_secret,
    namespace_pods_with_volumes,
)
def describe_appstore_namespace():
    def should_have_something(namespace: Namespace):
        assert "secret" in namespace.secrets
        assert "mypod" in namespace.pods

    def every_service_pod_should_have_something(namespace: Namespace):
        for pod in namespace.pods[rx("my-service-pod-pattern.*")]:
            assert "my-volume" in pod.volumes
            volume = pod.volumes["my-volume"]
            assert volume.nfs == "something meaningful"
```

## Run the tests for your namespace only

```shell
$ make test MARKERS="mynamespace"
```

Output would look like:

```
tests/kubernetes/appstore/test_appstore.py:

Appstore namespace:

  Healthy namespace:
    ✓ Has healthy pod[server]

  Namespace pods with volumes:
    ✓ Pods has expected volumes[server appstore-conf]
    ✓ Pods has expected volumes[server kube-api-access

  Namespace with tls secret:
    » Has tls secret  
```

## Contributing to the framework
* Missing some k8s object or some DSL-like operation? Add to [k8satisfying](k8satisfying) - wrapper for python k8s client.
* Want to make your custom tests a shared behaviour? Add to [k8spec/traits.py](k8spec/traits.py)
* `namespace.yaml` does not describe the traits of your namespace? Add to [k8spec/config.py](k8spec/config.py), make sure added properties are optional.
* it's all wrong, needs a total refactoring? Send the PR or contact the authors.

## Before opening a pull request

* Make sure your tests pass against the representative environment. Note that cloud-qa is different from production environments in sooo many ways.
* Format your code to comply with enforced code style:

```shell
$ make format
```

* Make sure style checks does not report any problems:

```shell
$ make style
```
