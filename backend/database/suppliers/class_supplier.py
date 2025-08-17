from typing import Union, Any, Dict
from dataclasses import dataclass

ID_FIELD_NAME = 'id'
SUPPLIER_FIELD_NAME = 'supplier'
DESCRIPTION_FIELD_NAME = 'destination'
ADDRESS_FIELD_NAME = 'address'
PHONE_FIELD_NAME = 'phono'
AMOUNT_FIELD_NAME = 'amount'

@dataclass
class Supplier:

    id: Union[int, None]
    supplier: Union[str, None]
    description: Union[str, None]
    address: Union[str, None]
    phone: Union[str, None]
    amount: Union[float, None]

    def __init__(self):
        self.id = None
        self.supplier = None
        self.description = None
        self.address = None
        self.phone = None
        self.amount = None


    def to_json_serializable(self) -> Dict[str, Any]:
        return {
            ID_FIELD_NAME: self.id,
            SUPPLIER_FIELD_NAME: self.supplier,
            DESCRIPTION_FIELD_NAME: self.description,
            ADDRESS_FIELD_NAME: self.address,
            PHONE_FIELD_NAME: self.phone,
            AMOUNT_FIELD_NAME: self.amount
        }