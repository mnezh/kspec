"""
Kubernetes IngressRule
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_ingress_rule import V1IngressRule

from k8satifying.base import KubernetesObjectList, KubernetesObjectWrapper


class IngressRule(KubernetesObjectWrapper, V1IngressRule):
    """Kubernetes secret"""

    @property
    def name(self) -> str:
        return self.host


class IngressRuleList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, IngressRule)

    def __getitem__(self, item) -> IngressRule | list[IngressRule]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[IngressRule, None, None]:
        return super().__iter__()
