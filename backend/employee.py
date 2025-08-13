from typing import Union, Any, Dict


class Employee:

    id: Union[int, None]
    name: Union[str, None]
    surname: Union[str, None]
    salary: Union[float, None]
    status: Union[float, None]

    def __init__(self):
        self.name = None
        self.surname = None
        self.salary = None
        self.status = None