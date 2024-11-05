"""
Kubernetes Deployment
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_deployment import V1Deployment

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class Deployment(KubernetesMetadataObjectWrapper, V1Deployment):
    """Kubernetes secret"""

    pass


class DeploymentList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Deployment)

    def __getitem__(self, item) -> Deployment | list[Deployment]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Deployment, None, None]:
        return super().__iter__()
