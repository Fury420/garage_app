from typing import Union, Any, Dict
from datetime import date
from dataclasses import dataclass


ID_FIELD_NAME = "id"
AMOUNT_FIELD_NAME = "amount"
DATE_FIELD_NAME = "date"

@dataclass
class Income:

    id: Union[int, None]
    amount: Union[float, None]
    date: Union[date, None]

    def __init__(self):
        self.id = None
        self.amount = None
        self.date = None

    def to_json_serializable(self) -> Dict[str, Any]:
        return {
            ID_FIELD_NAME: self.id,
            AMOUNT_FIELD_NAME: self.amount,
            DATE_FIELD_NAME: self.date
        }