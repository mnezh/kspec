"""
Testing framework for Kubernetes clusters based on:
* pytest-describe plugin https://github.com/pytest-dev/pytest-describe
* k8satisfying wrapper around the official python kubernetes client
"""
from pytest_describe import behaves_like as like

from k8spec.pytest import (
    aws,
    azure,
)
from k8spec.util import mark, rx
