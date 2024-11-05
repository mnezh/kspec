"""
Kubernetes Container
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_container import V1Container

from k8satifying.base import KubernetesObjectList, KubernetesObjectWrapper


class Container(KubernetesObjectWrapper, V1Container):
    """Kubernetes secret"""

    pass


class ContainerList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Container)

    def __getitem__(self, item) -> Container | list[Container]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Container, None, None]:
        return super().__iter__()
