"""
Convenience wrapper around the official python kubernetes client.
(https://github.com/kubernetes-client/python)

Extends k8s model objects returned by API calls with DSL-like methods.
"""
from k8satifying.cluster import Cluster
from k8satifying.config_map import ConfigMap, ConfigMapList
from k8satifying.container import Container, ContainerList
from k8satifying.deployment import Deployment, DeploymentList
from k8satifying.ingress import Ingress, IngressList
from k8satifying.namespace import Namespace
from k8satifying.persistent_volume_claim import (
    PersistentVolumeClaim,
    PersistentVolumeClaimList,
)
from k8satifying.pod import Pod, PodList
from k8satifying.secret import Secret, SecretList
from k8satifying.service import Service, ServiceList
from k8satifying.service_account import ServiceAccount, ServiceAccountList
from k8satifying.volume import Volume, VolumeList
