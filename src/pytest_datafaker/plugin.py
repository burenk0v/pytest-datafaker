"""Pytest plugin for generate test steps on HIVE dashboard."""

import pkgutil
from importlib import import_module

import pytest
from _pytest.config import Config

from . import fixtures


SEED_OPTION_NAME = "datafaker-seed"


def pytest_addoption(parser: pytest.Parser):
    """Pytest add option."""
    parser.addoption(
        f"--{SEED_OPTION_NAME}",
        action="store",
        default=None,
        help="Seed used for deterministic test data generation.",
    )


def pytest_configure(config: Config):
    """Configure pytest."""
    # Register fixture modules in pytest.
    if hasattr(fixtures, "__path__"):
        for fixture in pkgutil.iter_modules(fixtures.__path__, fixtures.__name__ + "."):
            config.pluginmanager.register(import_module(fixture.name))
    else:
        config.pluginmanager.register(fixtures, "pytest_datafaker.fixtures")
