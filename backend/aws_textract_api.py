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

TEST_INVOICE_PATH = "./mindee_test_data/vlcie_sirupy.jpg"


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
            connect_timout=10,
            read_timeout=30
        )
    )

def convert_and_compress(file_bytes: bytes) -> bytes:
    pass # TODO


def test_run():
    textract_client = get_textract_client()
    try:
        with open(TEST_INVOICE_PATH, "rb") as file:
            file_bytes = file.read()
        response = textract_client.analyze_expense(
            Document={
                "Bytes": convert_and_compress(file_bytes)
            }
        )
        # A blob of base64-encoded document bytes.
        # The maximum size of a document that’s provided in a blob of bytes is 5 MB.
        # The document bytes must be in PNG or JPEG format.
    except OSError as e:
        print(f"{e.__class__.__name__} : {e.args}")
    except BotoCoreError as e:
        print(f"{e.__class__.__name__} : {e.args}")
