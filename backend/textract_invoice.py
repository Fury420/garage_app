from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from textract_invoice_item import InvoiceItem
from typing import List, Optional


SUPPORTED_CURRENCIES: List[str] = [
    "USD", "EUR", "GBP", "CAD", "INR", "JPY", "CHF", "AUD", "CNY", "BZR", "SEK", "HKD"
]


@dataclass
class Invoice:
    """Represents a complete invoice"""
    invoice_number: str
    invoice_date: datetime
    vendor_name: str
    vendor_ico: str
    vendor_dic: str
    sub_total: Decimal  # Total before tax
    total: Decimal  # Final amount to pay
    currency: str = "EUR"
    items: List[InvoiceItem] = field(default_factory=list)
    due_date: Optional[datetime] = None
    vendor_address: Optional[str] = None
    vendor_bank_account: Optional[str] = None
    payment_method: Optional[str] = None

