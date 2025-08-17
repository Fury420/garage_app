import base64
import datetime
import io
from boto3 import client
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

TEST_INVOICE_PATH = "./test_data/vlcie_sirupy.jpg"


def get_textract_client() -> client:
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

def convert_and_compress(file_bytes: bytes, mime: str) -> bytes | None:
    if mime == "application/pdf":
        try:
            images = convert_from_bytes(
                file_bytes,
                first_page=1,
                last_page=1,
                dpi=200,
                fmt="jpeg"
            )
            if not images:
                raise ValueError("PDF conversion failed")
            pil_image = images[0]
        except Exception as e:
            print(f"{e.__class__.__name__} : {e.args}")
            return None
    else:
        try:
            pil_image = Image.open(io.BytesIO(file_bytes))
            if pil_image.mode in ("RGBA", "P", "LA"):
                pil_image = pil_image.convert("RGB")
        except Exception as e:
            print(f"{e.__class__.__name__} : {e.args}")
            return None
    pil_image.thumbnail((1080, 1920), Image.Resampling.LANCZOS)
    out_buffer = io.BytesIO()
    pil_image.save(out_buffer, format="JPEG", quality=85)
    # TODO should be less than 5MB, but check just to be sure
    return out_buffer.getvalue()


def test_run():
    textract_client = get_textract_client()
    try:
        with Image.open(TEST_INVOICE_PATH, "r") as pil_image:
            pil_image.convert("RGB")
            output_buffer = io.BytesIO()
            pil_image.save(output_buffer, format="JPEG", quality=85)
        jpeg_bytes = output_buffer.getvalue()
        response = textract_client.analyze_expense(
            Document={
                "Bytes": base64.b64encode(jpeg_bytes).decode('utf-8')
            }
        )
        # A blob of base64-encoded document bytes.
        # The maximum size of a document that’s provided in a blob of bytes is 5 MB.
        # The document bytes must be in PNG or JPEG format.
        with open("./test_run_out.json", "w") as out_file:
            json.dump(response, out_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    except BotoCoreError as e:
        print(f"{e.__class__.__name__} : {e.args}")


if __name__ == '__main__':
    """
    test_run()
    
    try:
        with open("./test_data/vlcie_sirupy.pdf", "rb") as in_file:
            filebytes = in_file.read()
        compressed_file = convert_and_compress(filebytes, "application/pdf")
        if compressed_file is None:
            raise ValueError("Compression failed")
        with open(f"./compression_out_{datetime.datetime.now().time().isoformat()}.jpeg", "wb") as out_file:
            out_file.write(compressed_file)
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    """
