"""
Dataclass representations of YAML configurations for clusters and namespaces
"""
from dataclasses import dataclass, field


@dataclass
class PodConfig:
    name: str
    volumes: list[str] = field(default_factory=list)


@dataclass
class SecretConfig:
    name: str
    type: str = "Opaque"
    data: dict[str | str] = field(default_factory=dict)


@dataclass
class NamespaceConfig:
    name: str
    pods: list[PodConfig] = field(default_factory=list)
    secrets: list[SecretConfig] = field(default_factory=list)
    tls_cn_pattern: str | None = None

    def __post_init__(self):
        if isinstance(self.pods, str):
            self.pods = [PodConfig(name=self.pods)]
        if isinstance(self.pods, dict):
            self.pods = [
                PodConfig(name=name, **(data or {})) for name, data in self.pods.items()
            ]
        if isinstance(self.secrets, str):
            self.secrets = [SecretConfig(name=self.secrets)]
        if isinstance(self.secrets, dict):
            self.secrets = [
                SecretConfig(name=name, data=data)
                for name, data in self.secrets.items()
            ]
