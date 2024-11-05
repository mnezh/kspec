"""
Kubernetes Ingress
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_ingress import V1Ingress

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList
from k8satifying.ingress_rule import IngressRuleList


class Ingress(KubernetesMetadataObjectWrapper, V1Ingress):
    """Kubernetes secret"""

    @property
    def rules(self) -> IngressRuleList:
        return IngressRuleList(self.k8s, self.spec.rules)


class IngressList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, Ingress)

    def __getitem__(self, item) -> Ingress | list[Ingress]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[Ingress, None, None]:
        return super().__iter__()
