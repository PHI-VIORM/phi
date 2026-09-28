"""Deterministic sampling for reproducible analysis previews."""

from __future__ import annotations

import random
from typing import TypeVar


T = TypeVar("T")


def sample(items: list[T], size: int, seed: int = 0) -> list[T]:
    if size < 0:
        raise ValueError("采样数量不能为负数")
    if size >= len(items):
        return list(items)
    generator = random.Random(seed)
    indexes = sorted(generator.sample(range(len(items)), size))
    return [items[index] for index in indexes]

