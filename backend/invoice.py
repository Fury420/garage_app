from mindee import InferenceResponse
from mindee.parsing.v2.field.simple_field import SimpleField
from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from datetime import date
from typing import Union, Any, Dict


DATE_FIELD_NAME = "date"
VENDOR_NAME_FIELD_NAME = "vendor_name"
INVOICE_NUMBER_FIELD_NAME = "invoice_number"
TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME = "total_amount_without_vat"
LINE_ITEMS_FIELD_NAME = "line_items"

LI_QUANTITY_FIELD_NAME = "quantity"
LI_UNIT_PRICE_FIELD_NAME = "unit_price"
LI_DESCRIPTION_FIELD_NAME = "description"
LI_ITEM_SEPARATOR = '*'
LI_ITEM_TAG_SEPARATOR = ':'


class InvoiceItem:
    """
    Represents an Invoice Item.
    """

    quantity: Union[int, None]
    unit_price: Union[float, None]
    description: Union[str, None]

    def __init__(self):
        self.quantity = None
        self.unit_price = None
        self.description = None


class Invoice:
    """
    Represents an Invoice.
    """

    date: Union[date, None]
    vendor_name: Union[str, None]
    invoice_number: Union[str, None]
    total_amount_without_vat: Union[float, None]
    line_items: Union[list[InvoiceItem], None]

    def __init__(self, resp: InferenceResponse):
        date_raw = resp.inference.result.fields.get(DATE_FIELD_NAME)
        if date_raw is not None and isinstance(date_raw, SimpleField) \
                and date_raw.value is not None and isinstance(date_raw.value, str):
            self.date = date.fromisoformat(date_raw.value)
        else:
            self.date = None
        vendor_name_raw = resp.inference.result.fields.get(VENDOR_NAME_FIELD_NAME)
        if vendor_name_raw is not None and isinstance(vendor_name_raw, SimpleField) \
                and vendor_name_raw.value is not None and isinstance(vendor_name_raw.value, str):
            self.vendor_name = vendor_name_raw.value
        else:
            self.vendor_name = None
        invoice_number_raw = resp.inference.result.fields.get(INVOICE_NUMBER_FIELD_NAME)
        if invoice_number_raw is not None and isinstance(invoice_number_raw, SimpleField) \
                and invoice_number_raw.value is not None and isinstance(invoice_number_raw.value, str):
            self.invoice_number = invoice_number_raw.value
        else:
            self.invoice_number = None
        total_amount_without_vat_raw = resp.inference.result.fields.get(TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME)
        if total_amount_without_vat_raw is not None and isinstance(total_amount_without_vat_raw, SimpleField) \
                and total_amount_without_vat_raw.value is not None \
                and isinstance(total_amount_without_vat_raw.value, float):
            self.total_amount_without_vat = total_amount_without_vat_raw.value
        else:
            self.total_amount_without_vat = None
        line_items_raw = resp.inference.result.fields.get(LINE_ITEMS_FIELD_NAME)
        if line_items_raw is not None and isinstance(line_items_raw, ListField):
            self.line_items = []
            for item in line_items_raw.items:
                if not isinstance(item, ObjectField):
                    continue
                invoice_item = InvoiceItem()
                quanity_raw = item.fields.get(LI_QUANTITY_FIELD_NAME)
                if quanity_raw is not None and isinstance(quanity_raw, SimpleField) \
                        and quanity_raw.value is not None and isinstance(quanity_raw.value, float):
                    invoice_item.quantity = int(quanity_raw.value)
                unit_price_raw = item.fields.get(LI_UNIT_PRICE_FIELD_NAME)
                if unit_price_raw is not None and isinstance(unit_price_raw, SimpleField) \
                        and unit_price_raw.value is not None and isinstance(unit_price_raw.value, float):
                    invoice_item.unit_price = unit_price_raw.value
                description_raw = item.fields.get(LI_DESCRIPTION_FIELD_NAME)
                if description_raw is not None and isinstance(description_raw, SimpleField) \
                        and description_raw.value is not None and isinstance(description_raw.value, str):
                    invoice_item.description = description_raw.value
                if invoice_item.quantity is not None or invoice_item.unit_price is not None \
                        or invoice_item.description is not None:
                    self.line_items.append(invoice_item)
        else:
            self.line_items = None

    def print_invoice_data(self):
        print(f"{DATE_FIELD_NAME}: {self.date}")
        print(f"{VENDOR_NAME_FIELD_NAME}: {self.vendor_name}")
        print(f"{INVOICE_NUMBER_FIELD_NAME}: {self.invoice_number}")
        print(f"{TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME}: {self.total_amount_without_vat}")
        if self.line_items is not None:
            for item in self.line_items:
                print(f"\n{LI_QUANTITY_FIELD_NAME}: {item.quantity}")
                print(f"{LI_UNIT_PRICE_FIELD_NAME}: {item.unit_price}")
                print(f"{LI_DESCRIPTION_FIELD_NAME}: {item.description}")

    def to_json_serializable(self) -> Dict[str, Any]:
        return {
            DATE_FIELD_NAME: self.date,
            VENDOR_NAME_FIELD_NAME: self.vendor_name,
            INVOICE_NUMBER_FIELD_NAME: self.invoice_number,
            TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME: self.total_amount_without_vat
        }
