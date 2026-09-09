"""Deterministic pseudo-random helpers for DataFaker."""

import random
from collections.abc import Sequence
from typing import TypeVar


T = TypeVar("T")


class RandomContext:
    """Seeded pseudo-random context for reproducible generation."""

    def __init__(self, seed: int):
        """Initialize the random context."""
        self._random = random.Random(seed)

    def choice(self, values: Sequence[T]) -> T:
        """Return a reproducible random item from a non-empty sequence."""
        return self._random.choice(values)

    def randint(self, a: int, b: int) -> int:
        """Return a reproducible random integer N such that a <= N <= b."""
        return self._random.randint(a, b)

    def random(self) -> float:
        """Return the next reproducible random float in the range [0.0, 1.0)."""
        return self._random.random()

    def randrange(self, start: int, stop: int | None = None, step: int = 1) -> int:
        """Return a reproducible random element from range(start, stop, step)."""
        if stop is None:
            return self._random.randrange(start)
        return self._random.randrange(start, stop, step)
