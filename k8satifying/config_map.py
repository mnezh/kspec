"""
Kubernetes ConfigMap
"""
from typing import Generator

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_config_map import V1ConfigMap

from k8satifying.base import KubernetesMetadataObjectWrapper, KubernetesObjectList


class ConfigMap(KubernetesMetadataObjectWrapper, V1ConfigMap):
    """Kubernetes secret"""

    pass


class ConfigMapList(KubernetesObjectList):
    """Typed list of kubernetes secrets"""

    def __init__(self, k8s: CoreV1Api, raw_list: list):
        super().__init__(k8s, raw_list, ConfigMap)

    def __getitem__(self, item) -> ConfigMap | list[ConfigMap]:
        return super().__getitem__(item)

    def __iter__(self) -> Generator[ConfigMap, None, None]:
        return super().__iter__()
