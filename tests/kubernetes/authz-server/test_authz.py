from k8spec import like, mark
from k8spec.traits import (
    healthy_namespace,
    namespace_with_secrets,
    namespace_yaml,
)

pytestmark = mark("authz")


@like(
    namespace_yaml(__file__),
    healthy_namespace,
    namespace_with_secrets,
)
def describe_authz_namespace():
    pass
