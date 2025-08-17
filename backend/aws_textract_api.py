from boto3 import client
from base64 import b64encode
from io import BytesIO
from datetime import datetime
from botocore.config import Config
from botocore.exceptions import BotoCoreError
from PIL import Image
from pdf2image import convert_from_bytes
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


def convert_and_compress(file_bytes: bytes, is_pdf: bool=False, pdf_page: int=1) -> bytes | None:
    """
    Converts PDF or image document to compressed JPEG image. If there is any issue with
    converting given document or final compressed document is larger than MAX_IMAGE_SIZE,
    method prints the exception to stdout and returns None.
    :param file_bytes: binary representation of PDF or image document
    :param is_pdf: specifies whether document is in PDF format
    :param pdf_page: specifies which PDF page we want to convert and compress
    :return: JPEG image in binary representation
    """
    # TODO: split method to image and pdf compression (we know content type from upload file)
    if is_pdf:
        try:
            images = convert_from_bytes(
                file_bytes,
                first_page=pdf_page,
                last_page=pdf_page,
                dpi=200,
                fmt="jpeg"
            )
            if not images:
                raise ValueError("PDF conversion failed")
            pil_image = images[pdf_page - 1]
        except Exception as e:
            print(f"{e.__class__.__name__} : {e.args}")
            return None
    else:
        try:
            pil_image = Image.open(BytesIO(file_bytes))
            if pil_image.mode in ("RGBA", "P", "LA"):
                pil_image = pil_image.convert("RGB")
        except Exception as e:
            print(f"{e.__class__.__name__} : {e.args}")
            return None
    pil_image.thumbnail((1080, 1920), Image.Resampling.LANCZOS)
    out_buffer = BytesIO()
    pil_image.save(out_buffer, format="JPEG", quality=85)
    print(out_buffer.getbuffer().nbytes)
    if out_buffer.getbuffer().nbytes >= MAX_IMAGE_SIZE:
        return None
    return out_buffer.getvalue()


def test_run() -> None:
    """
     Sends test request to textract service.
    """
    textract_client = get_textract_client()
    try:
        with open(TEST_INVOICE_PATH, "rb") as test_file:
            jpeg_bytes = convert_and_compress(test_file.read())
        response = textract_client.analyze_expense(
            Document={
                "Bytes": b64encode(jpeg_bytes).decode('utf-8')
            }
        )
        with open("./test_run_out.json", "w") as out_file:
            json.dump(response, out_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    except BotoCoreError as e:
        print(f"{e.__class__.__name__} : {e.args}")


if __name__ == '__main__':
    """
    test_run()
    """
    try:
        with open("./test_data/vlcie_sirupy.pdf", "rb") as in_file:
            filebytes = in_file.read()
        compressed_file = convert_and_compress(filebytes, is_pdf=True)
        if compressed_file is None:
            raise ValueError("Compression failed")
        with open(f"./compression_out_{datetime.now().time().isoformat()}.jpeg", "wb") as out_file:
            out_file.write(compressed_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
