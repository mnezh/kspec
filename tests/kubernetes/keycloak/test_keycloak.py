from k8spec import like, mark
from k8spec.traits import (
    healthy_namespace,
    namespace_with_secrets,
    namespace_with_tls_secret,
    namespace_yaml,
)

pytestmark = mark("keycloak")


@like(
    namespace_yaml(__file__),
    healthy_namespace,
    namespace_with_secrets,
    namespace_with_tls_secret,
)
def describe_keycloak_namespace():
    pass
