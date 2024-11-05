import base64
from urllib.parse import urlparse

from glom import glom
from pytest import fixture, skip

from k8satifying import ConfigMap, Deployment, Ingress, Namespace, Pod
from k8spec import like, mark, rx
from k8spec.traits import (
    healthy_namespace,
    namespace_with_secrets,
    namespace_with_tls_secret,
    namespace_yaml,
)

pytestmark = mark("appstore")

@like(
    namespace_yaml(__file__),
    namespace_with_secrets,
    healthy_namespace,
    namespace_with_tls_secret,
)
def describe_appstore_namespace():
    @fixture
    def server_deployment(namespace: Namespace, appstore_prefix: str) -> Deployment:
        assert rx(f".*{appstore_prefix}-server") in namespace.deployments
        return namespace.deployments[rx(f".*{appstore_prefix}-server")][0]

    @fixture
    def conf_config_map(namespace: Namespace, appstore_prefix: str) -> ConfigMap:
        assert rx(f".*{appstore_prefix}-conf") in namespace.config_maps
        return namespace.config_maps[rx(f".*{appstore_prefix}-conf")][0]

    def has_server_deployment(namespace: Namespace, server_deployment: Deployment):
        assert (
            server_deployment.status.available_replicas
            == server_deployment.status.replicas
        )

    def has_server_config_map(conf_config_map: ConfigMap):
        assert "q8s.toml" in conf_config_map.data

    def has_appstore_service_listening_to_http_port(namespace: Namespace, appstore_prefix: str):
        http_port = 80
        assert rx(f".*{appstore_prefix}-service") in namespace.services
        service = namespace.services[rx(f".*{appstore_prefix}-service")][0]
        assert any((port for port in service.spec.ports if port.port == http_port))

    def describe_ingress():
        @fixture
        def hac_ingress(namespace: Namespace, appstore_prefix: str) -> Ingress:
            assert rx(f"{appstore_prefix}.*ingress") in namespace.ingresses
            return namespace.ingresses[rx(f"{appstore_prefix}.*ingress")][0]

        def has_rules(hac_ingress: Ingress, appstore_prefix: str):
            wildcard_rule = hac_ingress.rules[rx(r"\*\..*")][0]
            base_url = wildcard_rule.name[2:]
            base_rule = hac_ingress.rules[base_url]
            assert f"{appstore_prefix}-service" in ",".join(
                glom(base_rule, "http.paths.*.backend.service.name")
            )
            assert f"{appstore_prefix}-service" in ",".join(
                glom(wildcard_rule, "http.paths.*.backend.service.name")
            )

    def has_service_account(namespace: Namespace, appstore_prefix: str):
        assert rx(f".*{appstore_prefix}.*service-account") in namespace.service_accounts

    def describe_server_pods():
        @fixture
        def server_pods(namespace: Namespace, appstore_prefix: str):
            return namespace.pods[rx(f".*{appstore_prefix}-server.*")]

        def pod_count_matches_deployment_replicas(
            server_deployment, server_pods: list[Pod]
        ):
            assert server_deployment.status.replicas == len(server_pods)

        def each_pod_has_config_map_mounted(server_pods: list[Pod], appstore_prefix: str):
            for pod in server_pods:
                server_container = pod.containers[f"{appstore_prefix}-server"]
                assert "/config" in glom(server_container.volume_mounts, ["mount_path"])

    def describe_appstore_postgresql():
        @fixture
        def pg_hostname(namespace: Namespace, appstore_prefix: str) -> str:
            dsn_encoded = namespace.secrets[rx(f".*{appstore_prefix}.*secrets")][0].data["dsn"]
            dsn = base64.b64decode(dsn_encoded).decode("utf-8")
            db_hostname = urlparse(dsn).hostname
            if "rds" in db_hostname:
                skip("No PostgreSQL deployed")
            return db_hostname

        def has_appstore_postgresql_secret(namespace: Namespace, pg_hostname: str, appstore_prefix: str):
            assert rx(f"{appstore_prefix}.*postgresql") in namespace.secrets

        def has_stateful_set(namespace: Namespace, appstore_prefix: str):
            assert rx(f"{appstore_prefix}.*postgresql") in namespace.statefulsets

    # TODO:
    # Cloud-qa and default setups doesn't use PVC
    # def describe_pvcs():
    #     def has_pvcs(namespace: Namespace):
    #         assert len(namespace.persistent_volume_claims) > 0
