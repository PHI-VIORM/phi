"""Small statistical helpers used by report consumers."""

from __future__ import annotations

import math


def percentile(values: list[float], percent: float) -> float:
    if not values:
        raise ValueError("无法计算空数据的百分位数")
    if not 0 <= percent <= 100:
        raise ValueError("百分位必须在 0 到 100 之间")
    ordered = sorted(values)
    position = (len(ordered) - 1) * percent / 100
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)

