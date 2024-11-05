from k8spec import like, mark
from k8spec.traits import (
    healthy_namespace,
    namespace_yaml,
)

pytestmark = mark("discovery")


@like(
    namespace_yaml(__file__),
    healthy_namespace,
)
def describe_discovery_namespace():
    pass
