"""Tax rates by country (Decimal, never float)."""

from __future__ import annotations
from decimal import Decimal

RATES: dict[str, Decimal] = {
    "AU": Decimal("0.10"),
    "GB": Decimal("0.20"),
    "US": Decimal("0.00"),  # state-level; out of scope for the demo
    "DE": Decimal("0.19"),
}


def rate_for(country_code: str) -> Decimal:
    return RATES.get(country_code.upper(), Decimal("0.00"))
