"""
Kubernetes pod
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_stateful_set import V1StatefulSet

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList

class StatefulSet(KubernetesMetadataObjectWrapper, V1StatefulSet):
    """Kubernetes pod"""

    pass


class StatefulSetList(KubernetesObjectList):
    """Typed list of kubernetes pods"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, StatefulSet)

    def __getitem__(self, item) -> StatefulSet | list[StatefulSet]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[StatefulSet, None, None]:
        return super().__iter__()
