"""Fixtures for pytest."""

import pytest

from .config import DataFakerConfig, get_config
from .datafaker import DataFaker


@pytest.fixture(scope="session", autouse=False)
def data_faker_config(pytestconfig: pytest.Config) -> DataFakerConfig:
    """Fixture for config."""
    seed = pytestconfig.getoption("--datafaker-seed", default=None, skip=False)
    return get_config(seed)


@pytest.fixture(scope="session", autouse=False)
def data_faker(data_faker_config: DataFakerConfig) -> DataFaker:
    """Fixture for faker module."""
    return DataFaker(data_faker_config)
