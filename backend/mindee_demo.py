from mindee import ClientV2, InferenceParameters, InferenceResponse
from pathlib import Path
import json

API_CONF_PATH = "./mindee_api_config.json"
API_CONF_API_KEY = "api_key"
API_CONF_MODEL_ID = "model_id"

DATE_FIELD_NAME = "date"
VAT_AMOUNT_FIELD_NAME = "vat_amount"
VENDOR_NAME_FIELD_NAME = "vendor_name"
TOTAL_AMOUNT_FIELD_NAME = "total_amount"
INVOICE_NUMBER_FIELD_NAME = "invoice_number"
LINE_ITEMS_FIELD_NAME = "line_items"
LI_QUANTITY_FIELD_NAME = "quantity"
LI_UNIT_PRICE_FIELD_NAME = "unit_price"
LI_DESCRIPTION_FIELD_NAME = "description"
LI_ITEM_SEPARATOR = '*'
LI_ITEM_TAG_SEPARATOR = ':'

TEST_INVOICE_PATH = "./mindee_test_data/vlcie_sirupy.pdf"

class Invoice:
    def __init__(self, resp: InferenceResponse):
        self.date: str | None = resp.inference.result.fields.get(DATE_FIELD_NAME)
        self.vat_amount: str | None = resp.inference.result.fields.get(VAT_AMOUNT_FIELD_NAME)
        self.vendor_name: str | None = resp.inference.result.fields.get(VENDOR_NAME_FIELD_NAME)
        self.total_amount: str | None = resp.inference.result.fields.get(TOTAL_AMOUNT_FIELD_NAME)
        self.invoice_number: str | None = resp.inference.result.fields.get(INVOICE_NUMBER_FIELD_NAME)
        self.line_items: list[dict[str, str]] | None = None
        self.__init_line_items__(resp)

    def __init_line_items__(self, resp: InferenceResponse) -> None:
        if resp.inference.result.fields.get(LINE_ITEMS_FIELD_NAME) is None:
            return None
        self.line_items = []
        known_prefixes: dict[str, str] = {
            LI_QUANTITY_FIELD_NAME : f"{LI_ITEM_TAG_SEPARATOR}{LI_QUANTITY_FIELD_NAME}{LI_ITEM_TAG_SEPARATOR}",
            LI_UNIT_PRICE_FIELD_NAME : f"{LI_ITEM_TAG_SEPARATOR}{LI_UNIT_PRICE_FIELD_NAME}{LI_ITEM_TAG_SEPARATOR}",
            LI_DESCRIPTION_FIELD_NAME : f"{LI_ITEM_TAG_SEPARATOR}{LI_DESCRIPTION_FIELD_NAME}{LI_ITEM_TAG_SEPARATOR}"}
        response_blocks: list[str] = (resp.inference.result.fields.get(LINE_ITEMS_FIELD_NAME)
                                      .multi_str().split(LI_ITEM_SEPARATOR))
        for block in response_blocks:
            item_dict: dict[str, str] = {}
            lines: list[str] = block.splitlines()
            for line in lines:
                stripped_line: str = line.strip()
                if not stripped_line:
                    continue
                elif stripped_line.startswith(known_prefixes[LI_QUANTITY_FIELD_NAME]):
                    item_dict[LI_QUANTITY_FIELD_NAME] = \
                        stripped_line[len(known_prefixes[LI_QUANTITY_FIELD_NAME]):].strip()
                elif stripped_line.startswith(known_prefixes[LI_UNIT_PRICE_FIELD_NAME]):
                    item_dict[LI_UNIT_PRICE_FIELD_NAME] = \
                        stripped_line[len(known_prefixes[LI_UNIT_PRICE_FIELD_NAME]):].strip()
                elif stripped_line.startswith(known_prefixes[LI_DESCRIPTION_FIELD_NAME]):
                    item_dict[LI_DESCRIPTION_FIELD_NAME] = \
                        stripped_line[len(known_prefixes[LI_DESCRIPTION_FIELD_NAME]):].strip()
            self.line_items.append(item_dict)
        return None

    def print_data(self):
        print(f"{DATE_FIELD_NAME}: {self.date}")
        print(f"{VAT_AMOUNT_FIELD_NAME}: {self.vat_amount}")
        print(f"{VENDOR_NAME_FIELD_NAME}: {self.vendor_name}")
        print(f"{TOTAL_AMOUNT_FIELD_NAME}: {self.total_amount}")
        print(f"{INVOICE_NUMBER_FIELD_NAME}: {self.invoice_number}")
        if self.line_items is not None:
            for item in self.line_items:
                if LI_QUANTITY_FIELD_NAME in item.keys():
                    print(f"\n{LI_QUANTITY_FIELD_NAME}: {item[LI_QUANTITY_FIELD_NAME]}")
                if LI_UNIT_PRICE_FIELD_NAME in item.keys():
                    print(f"{LI_UNIT_PRICE_FIELD_NAME}: {item[LI_UNIT_PRICE_FIELD_NAME]}")
                if LI_DESCRIPTION_FIELD_NAME in item.keys():
                    print(f"{LI_DESCRIPTION_FIELD_NAME}: {item[LI_DESCRIPTION_FIELD_NAME]}")

def get_configuration() -> tuple[str, str]:
    with open(API_CONF_PATH, "r") as config_file:
        config = json.load(config_file)
    return config[API_CONF_API_KEY], config[API_CONF_MODEL_ID]

if __name__ == '__main__':

    # configuration
    api_key, model_id = get_configuration()

    # initialize a new mindee client
    mindee_client: ClientV2 = ClientV2(api_key)

    # set inference parameters
    params = InferenceParameters(
        model_id=model_id,
        rag=False,
        alias=None,
        webhook_ids=None,
        polling_options=None,
        close_file=True)

    # load file from disk to mindee client instance
    input_source = mindee_client.source_from_path(
        input_path=Path(TEST_INVOICE_PATH),
        fix_pdf=False)

    # compression for pdfs
    # input_source.compress(quality=85)
    # WARNING:mindee.pdf.pdf_compressor:Found text inside of the provided PDF file.
    # Compression operation aborted since disableSourceText is set to 'true'.

    # if a pdf has more than one page, this could be useful
    # from mindee import PageOptions
    # input_source.apply_page_options(PageOptions(operation="KEEP_ONLY", page_indexes=[0]))

    # compression for images:
    # input_source.compress(quality=85, max_width=1920, max_height=1080)

    # send file for processing, get a response
    response = mindee_client.enqueue_and_get_inference(input_source, params)

    # create invoice class instance (sets all fields in __init__ method)
    invoice: Invoice = Invoice(response)

    # print retrieved data
    invoice.print_data()

