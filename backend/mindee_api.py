from mindee import ClientV2, InferenceParameters
from mindee.error.mindee_error import MindeeError
from backend.database.invoices.class_invoice import Invoice
from pathlib import Path
from typing import Tuple
import json


API_CONF_PATH = "../test_api_dir/mindee_api_config.json"
API_CONF_API_KEY = "api_key"
API_CONF_MODEL_ID = "model_id"

TEST_INVOICE_PATH = "./mindee_test_data/vlcie_sirupy.pdf"


def get_api_configuration() -> tuple[str, str]:
    """
    Retrieves api_key and model_id from .json config file specified by API_CONF_PATH.
    """

    with open(API_CONF_PATH, "r") as config_file:
        config = json.load(config_file)
    return config[API_CONF_API_KEY], config[API_CONF_MODEL_ID]


def get_client_and_params() -> Tuple[ClientV2, InferenceParameters]:
    """
    Retrieves API condfiguration and creates a client and parameters necessary
    for sending requests to Mindee OCR.
    """

    api_key, model_id = get_api_configuration()
    return ClientV2(api_key=api_key), InferenceParameters(model_id=model_id, close_file=True)


def run_test_request() -> None:
    """
     Sends a request to Mindee OCR using a documentent specified by TEST_INVOICE_PATH
     and prints the processed data to standard output.
    """

    client, params = get_client_and_params()
    input_source = client.source_from_path(input_path=Path(TEST_INVOICE_PATH), fix_pdf=False)
    try:
        response = client.enqueue_and_get_inference(input_source=input_source, params=params)
        invoice = Invoice(response)
        invoice.print_invoice_data()
    except MindeeError as e:
        print(e.__class__.__name__)


"""
if __name__ == '__main__':

    # retrieve api_key, model_id from .json config file
    api_key, model_id = get_api_configuration()

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
        polling_options=None,
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
"""
