"""
Kubernetes volume
"""

from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_volume import V1Volume

from k8satifying.base import KubernetesObjectList, KubernetesObjectWrapper


class Volume(KubernetesObjectWrapper, V1Volume):
    """Kubernetes volume"""

    pass


class VolumeList(KubernetesObjectList):
    """Typed list of kubernetes volumes"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Volume)

    def __getitem__(self, item) -> Volume:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Volume, None, None]:
        return super().__iter__()
