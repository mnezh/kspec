"""
Kubernetes PersistentVolumeClaim
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_persistent_volume_claim import V1PersistentVolumeClaim

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class PersistentVolumeClaim(KubernetesMetadataObjectWrapper, V1PersistentVolumeClaim):
    """Kubernetes secret"""

    pass


class PersistentVolumeClaimList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, PersistentVolumeClaim)

    def __getitem__(self, item) -> PersistentVolumeClaim | list[PersistentVolumeClaim]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[PersistentVolumeClaim, None, None]:
        return super().__iter__()
