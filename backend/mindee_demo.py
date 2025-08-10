from mindee import ClientV2, InferenceParameters, InferenceResponse
from mindee.parsing.v2.field.simple_field import SimpleField
from mindee.parsing.v2.field.list_field import ListField
from mindee.parsing.v2.field.object_field import ObjectField
from mindee.input.polling_options import PollingOptions
from mindee.error.mindee_error import MindeeError
from pathlib import Path
from datetime import date
from typing import Union
import json


API_CONF_PATH = "./mindee_api_config.json"
API_CONF_API_KEY = "api_key"
API_CONF_MODEL_ID = "model_id"

DATE_FIELD_NAME = "date"
VAT_AMOUNT_FIELD_NAME = "vat_amount"
VENDOR_NAME_FIELD_NAME = "vendor_name"
TOTAL_AMOUNT_FIELD_NAME = "total_amount"
INVOICE_NUMBER_FIELD_NAME = "invoice_number"
TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME = "total_amount_without_vat"
LINE_ITEMS_FIELD_NAME = "line_items"

LI_QUANTITY_FIELD_NAME = "quantity"
LI_UNIT_PRICE_FIELD_NAME = "unit_price"
LI_DESCRIPTION_FIELD_NAME = "description"
LI_ITEM_SEPARATOR = '*'
LI_ITEM_TAG_SEPARATOR = ':'

TEST_INVOICE_PATH = "./mindee_test_data/vlcie_sirupy.pdf"


class InvoiceItem:

    quantity: Union[int, None]
    unit_price: Union[float, None]
    description: Union[str, None]

    def __init__(self):
        self.quantity = None
        self.unit_price = None
        self.description = None


class Invoice:

    date: Union[date, None]
    vat_amount: Union[float, None]
    vendor_name: Union[str, None]
    total_amount: Union[float, None]
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
        vat_amount_raw = resp.inference.result.fields.get(VAT_AMOUNT_FIELD_NAME)
        if vat_amount_raw is not None and isinstance(vat_amount_raw, SimpleField) \
                and vat_amount_raw.value is not None and isinstance(vat_amount_raw.value, float):
            self.vat_amount = vat_amount_raw.value
        else:
            self.vat_amount = None
        vendor_name_raw = resp.inference.result.fields.get(VENDOR_NAME_FIELD_NAME)
        if vendor_name_raw is not None and isinstance(vendor_name_raw, SimpleField) \
                and vendor_name_raw.value is not None and isinstance(vendor_name_raw.value, str):
            self.vendor_name = vendor_name_raw.value
        else:
            self.vendor_name = None
        total_amount_raw = resp.inference.result.fields.get(TOTAL_AMOUNT_FIELD_NAME)
        if total_amount_raw is not None and isinstance(total_amount_raw, SimpleField) \
                and total_amount_raw.value is not None and isinstance(total_amount_raw.value, float):
            self.total_amount = total_amount_raw.value
        else:
            self.total_amount = None
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
        print(f"{VAT_AMOUNT_FIELD_NAME}: {self.vat_amount}")
        print(f"{VENDOR_NAME_FIELD_NAME}: {self.vendor_name}")
        print(f"{TOTAL_AMOUNT_FIELD_NAME}: {self.total_amount}")
        print(f"{INVOICE_NUMBER_FIELD_NAME}: {self.invoice_number}")
        print(f"{TOTAL_AMOUNT_WITHOUT_VAT_FIELD_NAME}: {self.total_amount_without_vat}")
        if self.line_items is not None:
            for item in self.line_items:
                print(f"\n{LI_QUANTITY_FIELD_NAME}: {item.quantity}")
                print(f"{LI_UNIT_PRICE_FIELD_NAME}: {item.unit_price}")
                print(f"{LI_DESCRIPTION_FIELD_NAME}: {item.description}")


def get_configuration() -> tuple[str, str]:
    with open(API_CONF_PATH, "r") as config_file:
        config = json.load(config_file)
    return config[API_CONF_API_KEY], config[API_CONF_MODEL_ID]


if __name__ == '__main__':

    # retrieve api_key, model_id from .json config file
    api_key, model_id = get_configuration()

    # create a mindee client instance that will send POST using mindee library
    # if an enviromental variable <MINDEE_V2_API_KEY> is set we can call ClientV2() instead
    client = ClientV2(api_key=api_key)

    # create parameters for sending POST request
    # model_id:         ID of mindee model [required]
    # rag:              Enable / Disable Retrieval-Augmented Generation [False by default]
    # alias:            An alias to link the file to your own DB [Optional]
    # webhook_ids:      IDs of webhooks to propagate the API response to [Optional]
    # polling_options:  Options for asynchronous polling [PollingOptions(2, 1.5, 80) by default]
    # close_file:       Whether to close the file after parsing [True by default]
    params = InferenceParameters(
        model_id=model_id,
        rag=True,
        alias=None,
        webhook_ids=None,
        polling_options=PollingOptions(initial_delay_sec=1, delay_sec=1, max_retries=50),
        close_file=True)

    # load a document from a path
    # input_path:   Path of file to open [required]
    # fix_pdf:      Whether to attempt fixing PDF files before sending [False by default]
    input_source = client.source_from_path(input_path=Path(TEST_INVOICE_PATH), fix_pdf=False)

    # compression for pdfs
    # input_source.compress(quality=85)
    # WARNING:mindee.pdf.pdf_compressor:Found text inside of the provided PDF file.
    # Compression operation aborted since disableSourceText is set to 'true'.

    # if a pdf has more than one page, this could be useful
    # from mindee import PageOptions
    # input_source.apply_page_options(PageOptions(operation="KEEP_ONLY", page_indexes=[0]))

    # compression for images:
    # input_source.compress(quality=85, max_width=1920, max_height=1080)

    try:
        # enqueue to an asynchronous endpoint and automatically poll for a response
        # input_source: The document/source file to use
        # params:       Parameters to set when sending a file
        response = client.enqueue_and_get_inference(input_source=input_source, params=params)

        # create invoice class instance (sets all fields in __init__ method)
        invoice = Invoice(response)

        # print retrieved data
        invoice.print_invoice_data()

    except MindeeError:
        # Invalid input source, parsing failed or couldn't retrieve document after <max_retries> retries
        pass

    # here we can reuse the same client to send another POST request
    # input_source = client.source_from_path(...)
    # response = client.enqueue_and_get_inference(...)
