"""
Kubernetes ServiceAccount
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_service_account import V1ServiceAccount

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class ServiceAccount(KubernetesMetadataObjectWrapper, V1ServiceAccount):
    """Kubernetes secret"""

    pass


class ServiceAccountList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, ServiceAccount)

    def __getitem__(self, item) -> ServiceAccount | list[ServiceAccount]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[ServiceAccount, None, None]:
        return super().__iter__()
