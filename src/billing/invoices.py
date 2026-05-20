"""Invoices module — Decimal arithmetic only. See .github/instructions/billing.instructions.md."""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int


@dataclass(frozen=True)
class Invoice:
    items: list[LineItem]
    customer_country: str


def subtotal(invoice: Invoice) -> Decimal:
    """Return the pre-tax subtotal of an invoice."""
    return sum((i.unit_price * i.quantity for i in invoice.items), Decimal("0"))


def apply_tax_to_invoice(invoice: Invoice) -> Decimal:
    """Return the grand total of `invoice`, including country-specific tax.

    Use rates from src/billing/tax.py. Round the grand total to 2 d.p. using
    banker's rounding (ROUND_HALF_EVEN). See billing.instructions.md.
    """
    # ⬅️ Demo will fill this in via Copilot Chat (see README Step 1 & 2).
    raise NotImplementedError
