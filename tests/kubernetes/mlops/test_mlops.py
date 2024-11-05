from k8spec import like, mark
from k8spec.traits import (
    healthy_namespace,
    namespace_with_secrets,
    namespace_yaml,
)

pytestmark = mark("mlops")


@like(
    namespace_yaml(__file__),
    healthy_namespace,
    namespace_with_secrets,
)
def describe_mlops_namespace():
    pass
