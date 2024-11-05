"""
Kubernetes Service
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_service import V1Service

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class Service(KubernetesMetadataObjectWrapper, V1Service):
    """Kubernetes secret"""

    pass


class ServiceList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Service)

    def __getitem__(self, item) -> Service | list[Service]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Service, None, None]:
        return super().__iter__()
