from mindee import InferenceResponse
from mindee.parsing.v2.field.simple_field import SimpleField
from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from datetime import date
from typing import Union, Any, Dict
from dataclasses import dataclass

DATE_FIELD_NAME = "date"
VENDOR_NAME_FIELD_NAME = "vendor_name"
TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME = "total_amount_without_vat"
LINE_ITEMS_FIELD_NAME = "line_items"

LI_QUANTITY_FIELD_NAME = "quantity"
LI_UNIT_PRICE_FIELD_NAME = "unit_price"
LI_DESCRIPTION_FIELD_NAME = "description"


@dataclass
class BillItem:

    id: Union[int, None]
    quantity: Union[int, None]
    unit_price: Union[float, None]
    description: Union[str, None]
    status: str

    def __init__(self):
        self.id = None
        self.quantity = None
        self.unit_price = None
        self.description = None
        self.status = 'Bill'



@dataclass
class Bill:

    date: Union[date, None]
    vendor_name: Union[str, None]
    total_amount_without_vat: Union[float, None]
    line_items: Union[list[BillItem], None]


    def to_json_serializable(self) -> Dict[str, Any]:
        return {
            DATE_FIELD_NAME: self.date,
            VENDOR_NAME_FIELD_NAME: self.vendor_name,
            TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME: self.total_amount_without_vat
        }