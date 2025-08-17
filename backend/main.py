from pathlib import Path
from mindee.error import MindeeError
from mindee_api import get_client_and_params, TEST_INVOICE_PATH
from backend.database.invoices.class_invoice import Invoice
from backend.database.database_connect import database


if __name__ == '__main__':

    client, params = get_client_and_params()
    input_source = client.source_from_path(input_path=Path(TEST_INVOICE_PATH), fix_pdf=False)
    try:
        response = client.enqueue_and_get_inference(input_source=input_source, params=params)
        invoice = Invoice(response)
        invoice.print_invoice_data()
        database(invoice)
    except MindeeError:
        print("Mindee Error")

