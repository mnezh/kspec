"""
Kubernetes pod
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_pod import V1Pod

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList
from k8satifying.container import ContainerList
from k8satifying.volume import VolumeList


class Pod(KubernetesMetadataObjectWrapper, V1Pod):
    """Kubernetes pod"""

    @property
    def containers(self):
        return ContainerList(self.k8s, self.spec.containers)

    @property
    def phase(self):
        """Which phase the pod is in"""
        return self.status.phase

    @property
    def volumes(self):
        """Volumes attached to the pod"""
        return VolumeList(self.k8s, self.spec.volumes)


class PodList(KubernetesObjectList):
    """Typed list of kubernetes pods"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Pod)

    def __getitem__(self, item) -> Pod | list[Pod]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Pod, None, None]:
        return super().__iter__()
