"""
Plugin for pytest. Provides:
* test configuration configuring via pytest CLI
* fixture for connecting to the k8s cluster
* cloud-specific markers (test tags)
"""
import pytest
import yaml
from _pytest.config.argparsing import Parser

from k8satifying.cluster import Cluster, ClusterConfig


def pytest_addoption(parser: Parser):
    group = parser.getgroup("k8sure", "Kubernetes tests")
    group.addoption(
        "--k8s-context",
        default=None,
        help="Override k8s context name",
    )

    group.addoption(
        "--env-config",
        type=open,
        default=None,
        help="YAML environment configuration to override defaults",
    )


@pytest.fixture(scope="session")
def k8s_config(request: pytest.FixtureRequest) -> ClusterConfig:
    env_config_file = request.config.getoption("--env-config")
    if env_config_file:
        config = ClusterConfig(**yaml.safe_load(env_config_file))
    else:
        config = ClusterConfig()

    if context_name := request.config.getoption("--k8s-context"):
        config.context = context_name
    return config


@pytest.fixture
def k8s_cluster(k8s_config: ClusterConfig) -> Cluster:
    return Cluster(k8s_config)


@pytest.fixture
def needs_azure(k8s_cluster: Cluster):
    if not k8s_cluster.is_azure:
        pytest.skip()


@pytest.fixture
def needs_aws(k8s_cluster: Cluster):
    if not k8s_cluster.is_aws:
        pytest.skip()


aws = pytest.mark.usefixtures("needs_aws")
azure = pytest.mark.usefixtures("needs_azure")
