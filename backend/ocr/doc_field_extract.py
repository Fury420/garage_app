import datetime
import re
from typing import Union

ICO_PATTERN = r"i[cč]o\s*[:;.-]*\s*[0-9]{8}"
DIC_PATTERN = r"di[cč]\s*[:;.-]*\s*[0-9]{10}"
IC_DPH_PATTERN = r"i[cč]\s+dph\s*[:;.-]*\s*SK[0-9]{10}"
INVOICE_NUMBER_PATTERN = r"fakt[uú]ra\s+[cč]\s*[:;.-]*\s*[0-9]+"
INVOICE_DATE_PATTERN = r"d[aá]tum\s+vyhotovenia\s*[:;.-]*\s*[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}"
INVOICE_DUE_DATE_PATTERN = r"d[aá]tum\s+splatnosti\s*[:;.-]*\s*[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}"
ICO_VALUE_PATTERN = r"[0-9]{8}"
DIC_VALUE_PATTERN = r"[0-9]{10}"
IC_DPH_VALUE_PATTERN = r"SK[0-9]{10}"
NUMBER_VALUE_PATTERN = r"[0-9]+"
DATE_VALUE_PATTERN = r"[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}"
DATE_FORMAT = "%d.%m.%Y"


def get_value_from_text(text, pattern, value_pattern):
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        value = re.search(value_pattern, match.group(), flags=re.IGNORECASE)
        if value:
            return value.group()
    return None


def get_ico(text: str) -> Union[str | None]:
    return get_value_from_text(text, ICO_PATTERN, ICO_VALUE_PATTERN)


def get_dic(text: str) -> Union[str | None]:
    return get_value_from_text(text, DIC_PATTERN, DIC_VALUE_PATTERN)


def get_ic_dph(text: str) -> Union[str | None]:
    return get_value_from_text(text, IC_DPH_PATTERN, IC_DPH_VALUE_PATTERN)


def get_invoice_number(text: str) -> Union[str, None]:
    return get_value_from_text(text, INVOICE_NUMBER_PATTERN, NUMBER_VALUE_PATTERN)


def get_invoice_date(text: str) -> Union[datetime.datetime, None]:
    return datetime.datetime.strptime(
        get_value_from_text(text, INVOICE_DATE_PATTERN, DATE_VALUE_PATTERN),
        DATE_FORMAT
    )


def get_invoice_due_date(text: str) -> Union[datetime.datetime, None]:
    return datetime.datetime.strptime(
        get_value_from_text(text, INVOICE_DUE_DATE_PATTERN, DATE_VALUE_PATTERN),
        DATE_FORMAT
    )


if __name__ == "__main__":

    with open("test_out/blahblahtext.txt", "r") as f:
        text1 = f.read()
    print(f"ico: {get_ico(text1)}")
    print(f"dic: {get_dic(text1)}")
    print(f"ic dph: {get_ic_dph(text1)}")
    print(f"invoice number: {get_invoice_number(text1)}")
    print(f"invoice date: {get_invoice_date(text1)}")
    print(f"invoice due date: {get_invoice_due_date(text1)}")
