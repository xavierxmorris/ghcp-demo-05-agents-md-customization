---
applyTo: "src/billing/**"
---

# Billing — instructions

Money is involved. These rules are non-negotiable for any code in
`src/billing/`.

## Numbers
- **Use `decimal.Decimal` for any monetary value.** Never `float`.
- Quantise totals with `Decimal("0.01")` and `ROUND_HALF_EVEN` (banker's
  rounding).
- Tax rates are stored as `Decimal` (e.g., `Decimal("0.10")`), never as 10.

## Errors
- Raise `BillingError` (or a subclass) from `src/billing/errors.py` —
  never bare `ValueError`.

## Tests
- Every monetary calculation needs at least one test that exercises rounding
  at the half-cent boundary (e.g., 0.005 → 0.00 with HALF_EVEN).

## Don't
- Don't add a dependency on `pandas` / `numpy` here — wrong tool.
- Don't `print()` — use `structlog`.
