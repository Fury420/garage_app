from typing import Union, Any, Dict
from datetime import date


class Income:

    id: Union[int, None]
    amount: Union[float, None]
    date: Union[date, None]

    def __init__(self):
        self.id = None
        self.amount = None
        self.date = None