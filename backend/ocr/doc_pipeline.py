import json
from doc_ocr import get_data_from_ocr
from doc_preprocess import preprocess_document
from doc_postprocess import process_ocr_data


TEST_DOCUMENT_PATH = "test_invoices/fckthem.pdf"
TEST_DOCUMENT_IS_PDF = True


def test_run() -> None:
    with open(TEST_DOCUMENT_PATH, "rb") as document_file:
        document_bytes = document_file.read()
    images = preprocess_document(document_bytes, TEST_DOCUMENT_IS_PDF)
    if images is None:
        raise ValueError("Preprocessing failed")
    ocr_data = get_data_from_ocr(images)
    document_text, document_data = process_ocr_data(ocr_data)
    with open("test_out/blahblahtext.txt", "w") as out_text_file:
        out_text_file.write(document_text)
        out_text_file.flush()
    with open("test_out/blahblahdata.json", "w") as out_json_file:
        json.dump(document_data, out_json_file, indent=4)
        out_json_file.flush()
    # TODO field extraction


if __name__ == "__main__":

    test_run()