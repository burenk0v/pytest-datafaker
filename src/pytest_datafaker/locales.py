"""Localization support."""

import locale
from enum import Enum


def _locales() -> dict[str, str]:
    """Create dict for emum."""
    result: dict[str, str] = {}
    for loc in locale.locale_alias:
        value = str(locale.locale_alias.get(loc)).split(".")[0]
        result[value.upper()] = value
    return result


# Create enum from locale aliases
Locales = Enum('Locales', _locales())  # type: ignore[misc]
