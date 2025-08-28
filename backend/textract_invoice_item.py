from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class InvoiceItem:
    """Represents a single line item on an invoice"""
    name: str
    quantity: Decimal
    unit_price: Decimal  # Price per unit before tax
    total_price: Decimal  # quantity * unit_price
    vat_rate: Optional[Decimal] = None  # VAT rate as percentage (e.g., 20.0 for 20%)
    vat_amount: Optional[Decimal] = None  # Calculated VAT amount
    unit_of_measure: Optional[str] = None  # e.g., "pcs", "kg", "hours"