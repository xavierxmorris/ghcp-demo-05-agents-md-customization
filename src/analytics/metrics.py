"""Analytics — vectorised, NumPy-first. See .github/instructions/analytics.instructions.md."""

from __future__ import annotations
import numpy as np


def mean(values) -> float:
    """Return the arithmetic mean of `values`. NaN for empty input."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return float("nan")
    return float(arr.mean())


# Demo Step 3: ask Copilot to add `percentile(values, p)` here.
