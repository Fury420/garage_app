from decimal import Decimal
from boto3 import client
from io import BytesIO
from datetime import datetime
from botocore.config import Config
from botocore.exceptions import BotoCoreError
from PIL import Image
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from typing import Union, Dict, Any, List, Optional
from textract_invoice import Invoice, InvoiceItem
from unidecode import unidecode
from re import findall, IGNORECASE, DOTALL
import json

AWS_CREDENTIALS_FILE = "./aws_credentials.json"
AWS_ACCESS_KEY_ID = "aws_access_key_id"
AWS_SECRET_ACCESS_KEY = "aws_secret_access_key"
AWS_DEFAULT_REGION = "aws_default_region"
AWS_TEXTRACT_SERVICE = "textract"

MAX_IMAGE_SIZE = 5242880    # 5MB

TEST_INVOICE_PATH = "./test_data/vlcie_sirupy.jpg"


def get_textract_client() -> client:
    """
    Creates a boto3.client instance using configuration in file specified by AWS_CREDENTIALS_FILE
    """
    try:
        with open(AWS_CREDENTIALS_FILE, "r") as credentials_file:
            credentials = json.load(credentials_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    return client(
        AWS_TEXTRACT_SERVICE,
        aws_access_key_id=credentials[AWS_ACCESS_KEY_ID],
        aws_secret_access_key=credentials[AWS_SECRET_ACCESS_KEY],
        config=Config(
            region_name=credentials[AWS_DEFAULT_REGION],
            retries={
                "max_attempts" : 5,
                "mode" : "standard"
            },
            connect_timeout=10,
            read_timeout=30
        )
    )


def pdf_to_jpeg(document_bytes: bytes) -> list[bytes] | None:
    """
    Converts given PDF document to JPEG images using pdf2image library. If conversion or image
    compression fails, method returns None.
    :param document_bytes: binary representation of PDF document
    :return: Compressed JPEG images in binary representation
    """
    pdf_reader = PdfReader(BytesIO(document_bytes))
    page_count = len(pdf_reader.pages)
    try:
        images = convert_from_bytes(
            document_bytes,
            first_page=1,
            last_page=page_count,
            dpi=200,
            fmt="jpeg"
        )
        if not images:
            raise ValueError("PDF conversion failed")
        compressed_images = []
        for image in images:
            compressed_images.append(compress_image(image))
            if compressed_images[-1] is None:
                raise ValueError(f"Compression failed on page: {len(compressed_images)}")
        return compressed_images
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")
        return None


def compress_image(image: Union[Image.Image | bytes]) -> bytes | None:
    """
    Compression of images using Pillow library. Image can be passed using binary representation [bytes] or
    the Pillow Image handle. The compression consists of converting image mode to RGB, resampling to
    1080x1920 resolution and finally JPEG compression [quality=85]. If any of said operations cause an exception,
    given image is not supported by Pillow library or the final compressed image is larger than MAX_IMAGE_SIZE,
    method returns None. The image handle is always closed by this method.
    :param image: image handle or binary representation of said image
    :return: Compressed JPEG image in binary representation.
    """
    if isinstance(image, bytes):
        try:
            pil_image = Image.open(BytesIO(image))
        except Exception as e:
            print(f"{e.__class__.__name__} : {e.args}")
            return None
    else:
        pil_image = image
    try:
        if pil_image.mode in ("RGBA", "P", "LA"):
            pil_image = pil_image.convert("RGB")
        pil_image.thumbnail((1080, 1920), Image.Resampling.LANCZOS)
        out_buffer = BytesIO()
        pil_image.save(out_buffer, format="JPEG", quality=85)
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")
        return None
    finally:
        pil_image.close()
    if out_buffer.getbuffer().nbytes < MAX_IMAGE_SIZE:
        return out_buffer.getvalue()
    return None


def create_invoice(response: Dict[Any, Any]) -> Invoice | None:
    """
    Creates Invoice class instance using given textract client response. If method fails
    to retrieve any of the attributes required by the Invoice class from given response,
    it returns None.
    :param response: valid Textract client response
    :return: Invoice class instance
    """
    expense_documents = response.get("ExpenseDocuments")
    if not isinstance(expense_documents, list) or len(expense_documents) < 1 or \
            not isinstance(expense_documents[0], dict):
        raise ValueError("ExpenseDocuments field missing, empty or in invalid format")
    expense_document = expense_documents[0]  # method expects only one document
    summary_fields = expense_document.get("SummaryFields")
    if not isinstance(summary_fields, list) or len(summary_fields) < 1:
        raise ValueError("SummaryFields field missing, empty or in invalid format")
    invoice_number = get_standard_field_value(
        summary_fields,
        "INVOICE_RECEIPT_ID",
        [
            r'cislo.*objednavky'
        ]
    )
    if invoice_number is None:
        raise ValueError("Invoice number missing")
    invoice_date = get_standard_field_value(
        summary_fields,
        "INVOICE_RECEIPT_DATE",
        [
            r'datum.*vystavenia'
        ]
    )
    if invoice_date is None:
        raise ValueError("Invoice date missing")
    try:
        invoice_date = datetime.fromisoformat(invoice_date.strip())
    except ValueError as e:
        raise ValueError(f"Failed to convert invoice date to datetime format: {e.args}")
    vendor_name = get_standard_field_value(
        summary_fields,
        "VENDOR_NAME",
        [
            r'dodavatel'
        ]
    )
    if vendor_name is None:
        raise ValueError("Vendor name missing")
    vendor_ico = get_standard_field_value(
        summary_fields,
        "TAX_PAYER_ID",
        [
            r'ico[:]?'
        ]
    )
    if vendor_ico is None:
        raise ValueError("Vendor ICO missing")
    vendor_dic = get_standard_field_value(
        summary_fields,
        "VENDOR_VAT_NUMBER",
        [
            r'dic[:]?'
        ]
    )
    if vendor_dic is None:
        raise ValueError("Vendor DIC missing")
    sub_total = get_standard_field_value(
        summary_fields,
        "SUBTOTAL",
        [
            r'bez.*dph.*celkovo',
            r'celkovo.*bez.*dph'
            r'celkova.*cena.*bez.*dph'
        ]
    )
    if sub_total is None:
        raise ValueError("Sub-total missing or in invalid format")
    # '32.51' or '32,51' pattern (at least one decimal digit before and after the '.' / ',' symbols)
    matches = findall(
        pattern=r'[0-9]+[.,][0-9]+',
        string=sub_total,
        flags=IGNORECASE | DOTALL
    )
    if len(matches) != 1:
        raise ValueError("Sub-total missing or in invalid format")
    sub_total = Decimal(matches[0])  # should not throw (defaults to 0.0 instead)
    total = get_standard_field_value(
        summary_fields,
        "TOTAL",
        [
            r'celkova.*cena',
            r'cena.*s.*dph'
            r'celkovo.*s.*dph'
        ]  # # maybe use [ \t\n\r\f\v]+ instead of .* to be more strict
    )
    if total is None:
        raise ValueError("Total missing or in invalid format")
    # '32.51' or '32,51' pattern (at least one decimal digit before and after the '.' / ',' symbols)
    matches = findall(
        pattern=r'[0-9]+[.,][0-9]+',
        string=total,
        flags=IGNORECASE | DOTALL
    )
    if len(matches) != 1:
        raise ValueError("Total missing or in invalid format")
    total = Decimal(matches[0].strip())  # should not throw (defaults to 0.0 instead)
    invoice = Invoice(invoice_number, invoice_date, vendor_name, vendor_ico, vendor_dic, sub_total, total)
    #  TODO fill Invoice with invoice items and other optional data
    return invoice


def get_standard_field_value(
        fields: List[Any], expected_type: str, expected_label_patterns: Optional[List[str]] = None
) -> str | None:
    for field in fields:
        if not isinstance(field, dict):
            continue
        value_field = field.get("ValueDetection")
        if not isinstance(value_field, dict) or not isinstance(value_field.get("Text"), str):
            continue
        type_field = field.get("Type")
        if isinstance(type_field, dict):
            type_field_value = type_field.get("Text")
            if isinstance(type_field_value, str) and type_field_value == expected_type:
                return value_field.get("Text")
            continue
        label_field = field.get("LabelDetection")
        if isinstance(label_field, dict):
            label_field_value = label_field.get("Text")
            if isinstance(label_field_value, str) and len(label_field_value) > 0:
                label_field_value_unicode = unidecode(label_field_value)
                for pattern in expected_label_patterns:
                    matches = findall(
                        pattern=pattern,
                        string=label_field_value_unicode,
                        flags=IGNORECASE | DOTALL
                    )
                    if len(matches) > 0:
                        return value_field.get("Text")
    return None



def test_run() -> None:
    """
     Sends test request to textract service.
    """
    textract_client = get_textract_client()
    try:
        with open(TEST_INVOICE_PATH, "rb") as test_file:
            payload = compress_image(test_file.read())
        response = textract_client.analyze_expense(
            Document={
                "Bytes": payload
            }
        )
        with open(f"./test_run{datetime.now().isoformat()}.json", "w") as out_file:
            json.dump(response, out_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    except BotoCoreError as e:
        print(f"{e.__class__.__name__} : {e.args}")


def run_tests() -> None:
    print("test multi-page PDF document")
    try:
        with open("../test_api_dir/test_data/homegym.pdf", "rb") as test_file:
            images = pdf_to_jpeg(test_file.read())
            for image_bytes in images:
                with open(f"../test_api_dir/test_out/homegym{datetime.now().isoformat()}.jpeg", "wb") as test_out_file:
                    test_out_file.write(image_bytes)
                    test_out_file.flush()
        print("OK")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")

    print("test single page PDF document")
    try:
        with open("../test_api_dir/test_data/martinus.pdf", "rb") as test_file:
            images = pdf_to_jpeg(test_file.read())
            for image_bytes in images:
                with open(f"../test_api_dir/test_out/martinus{datetime.now().isoformat()}.jpeg", "wb") as test_out_file:
                    test_out_file.write(image_bytes)
                    test_out_file.flush()
        print("OK")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")

    print("test image converted to PDF")
    try:
        with open("../test_api_dir/test_data/vlcie_sirupy.pdf", "rb") as test_file:
            images = pdf_to_jpeg(test_file.read())
            for image_bytes in images:
                with open(f"../test_api_dir/test_out/vlcie_sirupy{datetime.now().isoformat()}.jpeg", "wb") as test_out_file:
                    test_out_file.write(image_bytes)
                    test_out_file.flush()
        print("OK")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")

    print("test PNG image")
    try:
        with open("../test_api_dir/test_data/scio_image.png", "rb") as test_file:
            image_bytes = compress_image(test_file.read())
            with open(f"../test_api_dir/test_out/scio_image{datetime.now().isoformat()}.jpeg", "wb") as test_out_file:
                test_out_file.write(image_bytes)
                test_out_file.flush()
        print("OK")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")

    print("test JPG image")
    try:
        with open("../test_api_dir/test_data/vlcie_sirupy.jpg", "rb") as test_file:
            image_bytes = compress_image(test_file.read())
            with open(f"../test_api_dir/test_out/vlcie_sirupy_image{datetime.now().isoformat()}.jpeg","wb") as test_out_file:
                test_out_file.write(image_bytes)
                test_out_file.flush()
        print("OK")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")


if __name__ == '__main__':
    """
    test_run()
    
    
    # should be global in the api implementation
    textract_client = get_textract_client()

    # we will receive an UploadFile from frontend instead
    filepath = "../test_api_dir/test_data/homegym.pdf"

    # api call should look similar to this:
    try:
        with open(filepath, "rb") as test_file:
            # obtain binary representation (we will get this with fastapi.UploadFile)
            file_bytes = test_file.read()

            # here we would call fastapi.UploadFile.content_type to determine type
            # for now we will use postfix to determine type
            if test_file.name.endswith(".pdf"):
                # if given document is in pdf format we must first convert and compress it
                compressed_images = pdf_to_jpeg(file_bytes)

                # now we proceed send every pdf page to textract service
                for image_bytes in compressed_images:
                    response = textract_client.analyze_expense(
                        Document={
                            "Bytes": b64encode(image_bytes).decode('utf-8')
                        }
                    )
                    # response should be json serializable - TODO save it, process it,...

            elif test_file.name.endswith((".jpeg", ".jpg", ".png", ".bmp", ".tiff")):
                # if given document is in image format supported by Pillow library we just need to compress it
                image_bytes = compress_image(file_bytes)

                # now we proceed to send compressed invoice to textract service
                response = textract_client.analyze_expense(
                    Document={
                        "Bytes": b64encode(image_bytes).decode('utf-8')
                    }
                )
                # response should be json serializable - TODO save it, process it,...
            else:
                raise ValueError("HTTP error code : invalid file format given")
    except Exception as e:
        print(f"{e.__class__.__name__} : {e.args}")
        # return appropriate HTTP response to frontend
    """

    """
    response : Dict
    response["DocumentMetadata"] : Dict
    response["DocumentMetadata"]["Pages"] : int
    response["ExpenseDocuments"] : List
    response["ExpenseDocuments"][i] : Dict
    response["ExpenseDocuments"][i]["SummaryFields"] : List
    response["ExpenseDocuments"][i]["SummaryFields"][i] : Dict
    response["ExpenseDocuments"][i]["SummaryFields"][i]["Type"]["Text"] : string
    response["ExpenseDocuments"][i]["SummaryFields"][i]["LabelDetection"]["Text"] : string
    response["ExpenseDocuments"][i]["SummaryFields"][i]["ValueDetection"]["Text"] : string
    response["ExpenseDocuments"][i]["SummaryFields"][i]["PageNumber"] : int
    response["ExpenseDocuments"][i]["SummaryFields"][i]["Currency"]["Code"] : string
    response["ExpenseDocuments"][i]["LineItemGroups"] : List
    response["ExpenseDocuments"][i]["LineItemGroups"][i] : Dict
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"] : List
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i] : Dict
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"] : List
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i] : Dict
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i]["Type"]["Text"] : string
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i]["LabelDetection"]["Text"] : string
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i]["ValueDetection"]["Text"] : string
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i]["PageNumber"] : int
    response["ExpenseDocuments"][i]["LineItemGroups"][i]["LineItems"][i]["LineItemExpenseFields"][i]["Currency"]["Code"] : string
    response["ExpenseDocuments"][i]["Blocks"] : List
    response["ExpenseDocuments"][i]["Blocks"][i] : Dict
    response["ExpenseDocuments"][i]["Blocks"][i]["BlockType"] : string
    response["ExpenseDocuments"][i]["Blocks"][i]["Text"] : string
    
    Currency code for detected currency. the current supported codes are:
    USD, EUR, GBP, CAD, INR, JPY, CHF, AUD, CNY, BZR, SEK, HKD
    
    len(response["ExpenseDocuments"]) should be equal to 1
    len(response["ExpenseDocuments"][i]["LineItemGroups"]) also seems to be equal to 1
    """
