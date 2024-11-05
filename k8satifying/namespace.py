"""
Kubernetes namespace
"""
from kubernetes.client import AppsV1Api, CoreV1Api, NetworkingV1Api
from kubernetes.client.models.v1_namespace import V1Namespace

from k8satifying.base import KubernetesMetadataObjectWrapper
from k8satifying.config_map import ConfigMapList
from k8satifying.deployment import DeploymentList
from k8satifying.ingress import IngressList
from k8satifying.persistent_volume_claim import PersistentVolumeClaimList
from k8satifying.pod import PodList
from k8satifying.stateful_set import StatefulSetList
from k8satifying.secret import SecretList
from k8satifying.service import ServiceList
from k8satifying.service_account import ServiceAccountList


class Namespace(KubernetesMetadataObjectWrapper, V1Namespace):
    def __init__(self, k8s: CoreV1Api, model_object) -> None:
        super().__init__(k8s, model_object)
        self.k8s_app = AppsV1Api()
        self.k8s_net = NetworkingV1Api()

    @property
    def config_maps(self) -> ConfigMapList:
        """Config maps in namespace"""
        return ConfigMapList(
            self.k8s, self.k8s.list_namespaced_config_map(namespace=self.name).items
        )

    @property
    def deployments(self) -> DeploymentList:
        """App deployments in namespace"""
        return DeploymentList(
            self.k8s, self.k8s_app.list_namespaced_deployment(namespace=self.name).items
        )

    @property
    def ingresses(self) -> IngressList:
        """Ingresses in namespace"""
        return IngressList(
            self.k8s, self.k8s_net.list_namespaced_ingress(namespace=self.name).items
        )

    @property
    def pods(self) -> PodList:
        """Pods in namespace"""
        return PodList(
            self.k8s, self.k8s.list_namespaced_pod(namespace=self.name).items
        )

    @property
    def persistent_volume_claims(self) -> PersistentVolumeClaimList:
        """PVCs in namespace"""
        return PersistentVolumeClaimList(
            self.k8s,
            self.k8s.list_namespaced_persistent_volume_claim(namespace=self.name).items,
        )

    @property
    def secrets(self) -> SecretList:
        """Secrets in namespace"""
        return SecretList(
            self.k8s, self.k8s.list_namespaced_secret(namespace=self.name).items
        )

    @property
    def services(self) -> ServiceList:
        """Services in namespace"""
        return ServiceList(
            self.k8s, self.k8s.list_namespaced_service(namespace=self.name).items
        )

    @property
    def service_accounts(self) -> ServiceAccountList:
        """Service accounts in namespace"""
        return ServiceAccountList(
            self.k8s,
            self.k8s.list_namespaced_service_account(namespace=self.name).items
        )

    @property
    def statefulsets(self) -> StatefulSetList:
        """StatefulSets in namespace"""
        return StatefulSetList(
            self.k8s,
            self.k8s_app.list_namespaced_stateful_set(namespace=self.name).items
        )
