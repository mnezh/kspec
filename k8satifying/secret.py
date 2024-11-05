"""
Kubernetes secret
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_secret import V1Secret

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class Secret(KubernetesMetadataObjectWrapper, V1Secret):
    """Kubernetes secret"""

    pass


class SecretList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Secret)

    def __getitem__(self, item) -> Secret | list[Secret]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Secret, None, None]:
        return super().__iter__()
