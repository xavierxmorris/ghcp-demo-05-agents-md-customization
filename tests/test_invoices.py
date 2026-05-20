from decimal import Decimal
from src.billing.invoices import LineItem, Invoice, subtotal


def test_subtotal_uses_decimal():
    inv = Invoice(
        items=[LineItem("A", Decimal("9.99"), 2), LineItem("B", Decimal("1.50"), 1)],
        customer_country="AU",
    )
    assert subtotal(inv) == Decimal("21.48")
