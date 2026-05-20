---
applyTo: "src/analytics/**"
---

# Analytics — instructions

This subtree is performance-sensitive and operates on numeric arrays.

## Libraries
- **Prefer `numpy`** for any vectorisable operation. Adding `numpy` to
  `requirements.txt` here is acceptable.
- For percentiles, use `numpy.percentile` (linear interpolation method =
  default) unless the function says otherwise.

## Numerical correctness
- Use `np.float64` consistently. Do not mix dtypes silently.
- Handle empty arrays explicitly — return `np.nan` rather than raising,
  unless a docstring says otherwise.

## Tests
- Compare floats with `pytest.approx(..., abs=1e-9)`.
