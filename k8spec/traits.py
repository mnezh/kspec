"""
Shared behaviors for namespaces
(see https://github.com/pytest-dev/pytest-describe#shared-behaviors)
"""

import base64

import allure
from cryptography.x509 import load_pem_x509_certificate
from pytest import fixture

from k8satifying import Cluster, Namespace, SecretList
from k8spec import azure, rx
from k8spec.config import PodConfig, SecretConfig
from k8spec.util import load_namespace_config, near


def namespace_yaml(path):
    """Namespace definition loaded from namespace.yaml"""
    ns = load_namespace_config(near(path, "namespace.yaml"))

    def describe_namespace():
        @fixture
        def namespace(k8s_cluster: Cluster) -> Namespace:
            return k8s_cluster.namespace(ns.name)

        @fixture
        def appstore_prefix(k8s_cluster: Cluster) -> str:
            return k8s_cluster.appstore_prefix()

        @fixture(params=ns.pods, ids=lambda pod: pod.name)
        def pod_config(request) -> PodConfig:
            return request.param

        @fixture(
            params=[(pod, vol) for pod in ns.pods for vol in pod.volumes],
            ids=lambda pv: f"{pv[0].name} {pv[1]}",
        )
        def pod_volume(request) -> tuple[PodConfig, str]:
            return request.param

        @fixture
        def pod_name(pod_config: PodConfig) -> str:
            return pod_config.name

        @fixture(params=ns.secrets, ids=lambda sec: sec.name)
        def wanted_secret(request) -> SecretConfig:
            return request.param

        @fixture
        def cn_pattern() -> str:
            return ns.tls_cn_pattern

    return describe_namespace


def healthy_namespace():
    """Namespace having healthy pods"""

    def has_healthy_pod(namespace: Namespace, pod_name: str):
        pods = namespace.pods[rx(f".*{pod_name}.*")]
        assert (
            len(pods) > 0
        ), f"At least one {pod_name} expected in {namespace=} {namespace.pods}"
        for pod in pods:
            allure.attach(str(pod), name=pod.name)
            assert pod.phase in [
                "Complete",
                "Running",
                "Succeeded",
            ], f"{pod.name} {pod.status=}"


def namespace_with_secrets():
    """Namespace having expected secrets with non-empty field values"""

    @fixture
    def secrets(namespace: Namespace) -> SecretList:
        return namespace.secrets

    def has_secret(secrets: SecretList, wanted_secret: SecretConfig):
        pattern = rx(f"{wanted_secret.name}")
        assert pattern in secrets, f"No secret matching {pattern} in {secrets.names()}"
        secret = secrets[pattern][0]
        print(secret)
        assert secret.type == wanted_secret.type
        for data_key in wanted_secret.data:
            assert data_key in secret.data, f"{secret.data.keys()=}"
            assert secret.data[
                data_key
            ], f"data.{data_key} is empty in {secret.metadata.name}"


def namespace_pods_with_volumes():
    """Namespace having volumes with expected names"""

    def pods_has_expected_volumes(
        namespace: Namespace, pod_volume: tuple[PodConfig, str]
    ):
        pod_config, volume_name = pod_volume
        for pod in namespace.pods[rx(pod_config.name)]:
            assert (
                rx(volume_name) in pod.volumes
            ), f"No volume {volume_name} in {pod.volumes}"


def namespace_with_tls_secret():
    """Namespace having TLS certificate secret with expected CN= value"""

    @azure
    def has_tls_secret(namespace: Namespace, cn_pattern: str):
        pattern = rx(f".*-tls")
        secret = [s for s in namespace.secrets if pattern.match(s.name)]
        assert secret
        assert secret[0].type == "kubernetes.io/tls"
        assert "tls.crt" in secret[0].data
        crt = load_pem_x509_certificate(base64.b64decode(secret[0].data["tls.crt"]))
        assert cn_pattern in crt.subject.rfc4514_string()



