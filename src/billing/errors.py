"""Domain exceptions for billing."""


class BillingError(Exception):
    """Base class for all billing errors."""


class UnsupportedCountryError(BillingError):
    pass
