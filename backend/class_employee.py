from typing import Union, Any, Dict

ID_FIELD_NAME = 'id'
NAME_FIELD_NAME = 'name'
SURNAME_FIELD_NAME = 'surname'
SALARY_FIELD_NAME = 'salary'
STATUS_FIELD_NAME = 'status'


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


    def to_json_serializable(self) -> Dict[str, Any]:
        return {
            NAME_FIELD_NAME: self.name,
            SURNAME_FIELD_NAME: self.surname,
            SALARY_FIELD_NAME: self.salary,
            STATUS_FIELD_NAME: self.status
        }