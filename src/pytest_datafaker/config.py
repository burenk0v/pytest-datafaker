"""DataFaker configuration."""

import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path
from time import time_ns

from mimesis.enums import Locale


DEFAULT_LOCALES: set[Locale] = {Locale.EN, Locale.RU}


@dataclass
class DataFakerConfig:
    """DataFaker config class."""

    seed: int | str
    locales: set[str] | None = None


def get_config_from_toml(toml_path: str | Path, seed: int) -> DataFakerConfig | None:
    """Get config from toml file."""
    if isinstance(toml_path, str):
        toml_path = Path(toml_path)
    toml_content = tomllib.loads(toml_path.read_text())
    config_dict = toml_content.get("tool", {}).get("pytest_datafaker", {})
    if not config_dict:
        logging.warning("No 'pytest_datafaker' section found in pyproject.toml")
        return None
    return DataFakerConfig(seed, config_dict.get("locales", DEFAULT_LOCALES))


def get_config(seed: int | str | None = None) -> DataFakerConfig:
    """Get config from pyproject.toml or default config."""
    defaul_seed = time_ns() % 2**32
    if seed is None:
        logging.warning("No seed provided, using default seed based on current timestamp")
        seed = defaul_seed
    elif not isinstance(seed, int):
        try:
            seed = int(seed)
        except ValueError:
            logging.warning(f"Invalid seed value '{seed}', using default seed")
            seed = defaul_seed
    if seed < 0:
        logging.warning(f"Negative seed value '{seed}', using default seed")
        seed = defaul_seed
    config = get_config_from_toml("pyproject.toml", seed)
    if not config:
        logging.warning("No config found in pyproject.toml, using default config")
        config = DataFakerConfig(seed=seed)
    return config
