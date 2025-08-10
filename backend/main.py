from pathlib import Path
from mindee.error import MindeeError
from mindee_demo import Invoice, InvoiceItem, get_configuration
from mindee import ClientV2, InferenceParameters, PollingOptions
from dat import database
import mindee_demo


if __name__ == '__main__':

    api_key, model_id = get_configuration()
    client = ClientV2(api_key)
    params = InferenceParameters(
        model_id=model_id,
        rag=True,
        alias=None,
        webhook_ids=None,
        polling_options=PollingOptions(initial_delay_sec=1, delay_sec=1, max_retries=50),
        close_file=True)
    input_source = client.source_from_path(input_path=Path(mindee_demo.TEST_INVOICE_PATH), fix_pdf=False)
    try:
        response = client.enqueue_and_get_inference(input_source=input_source, params=params)
        invoice = Invoice(response)
        invoice.print_invoice_data()
        database(invoice)
    except MindeeError:
        print("Mindee Error")

