"""
Convience methods used in tests and framework
"""
import pathlib
import re

import pytest
import yaml

from k8spec.config import NamespaceConfig


def near(path: str, filename: str) -> str:
    """Path to the file in the same directory"""
    return pathlib.Path(path).parent / filename


def load_namespace_config(yaml_path: str) -> NamespaceConfig:
    """Read and parse namespace config from yaml file"""
    with open(yaml_path) as f:
        return NamespaceConfig(**yaml.safe_load(f))


def mark(mark_name: str):
    """brief alias for pytest mark (test tag)"""
    return pytest.mark.__getattr__(mark_name)()


def rx(pattern: str) -> re.Pattern:
    """brief alias for regex compiler"""
    return re.compile(pattern)
