"""
Kubernetes cluster
"""
from dataclasses import dataclass, field

import kubernetes

from k8satifying.namespace import Namespace


@dataclass
class ClusterConfig:
    """Replicated Cluster configuration defines context and namespace name overrides"""

    context: str | None = None
    appstore_prefix: str | None = "appstore"
    namespaces: dict[str, str] = field(default_factory=dict)


class Cluster:
    """Replicated Kubernetes cluster"""

    def __init__(self, config: ClusterConfig) -> None:
        self.config = config
        kubernetes.config.load_kube_config(context=config.context)
        self.k8s = kubernetes.client.CoreV1Api()

    @property
    def host(self) -> str:
        """Kubernetes API endpoint host name"""
        return self.k8s.api_client.configuration.host

    @property
    def is_azure(self) -> bool:
        """Does kubernetes API endpoint host name look like Azure?"""
        return "azmk8s.io" in self.host

    @property
    def is_aws(self) -> bool:
        """Does kubernetes API endpoint host name look like AWS?"""
        return "eks.amazon" in self.host

    def namespace(self, name) -> Namespace:
        """Get kubernetes namespace by name"""
        namespace_name = self.config.namespaces.get(name, name)
        return Namespace(self.k8s, self.k8s.read_namespace(namespace_name))

    def appstore_prefix(self) -> str:
        """Get appstore objects prefix"""
        return self.config.appstore_prefix
