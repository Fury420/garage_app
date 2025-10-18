from pytesseract import pytesseract


TESSERACT_CONF_DPI = r'--dpi 300'
TESSERACT_CONF_PSM = r'--psm 6'
TESSERACT_CONF_OEM = r'--oem 3'
TESSERACT_CONF_PRESERVE_INTERWORD_SPACES = r'-c preserve_interword_spaces=1'
TESSERACT_CONF_TEXTORD_TABFIND_VERTICAL_TEXT = r'-c textord_tabfind_vertical_text=0'
TESSERACT_CONF_TEXTORD_MAKE_PROP_WORDS = r'-c textord_make_prop_words=1'
TESSERACT_CONF_TEXTORD_NO_REJECTS = r'-c textord_no_rejects=1'
TESSERACT_CONF_TESSEDIT_CHAR_WHITELIST = r'-c tessedit_char_whitelist=0123456789.,abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZščťžýáíéúäňôľřěďŠČŤŽÝÁÍÉÚÄŇÔĽŘĚĎ-+/():%€ '
TESSERACT_CONFIG = f'{TESSERACT_CONF_DPI} {TESSERACT_CONF_PSM} {TESSERACT_CONF_OEM} {TESSERACT_CONF_PRESERVE_INTERWORD_SPACES} {TESSERACT_CONF_TEXTORD_TABFIND_VERTICAL_TEXT} {TESSERACT_CONF_TEXTORD_MAKE_PROP_WORDS} {TESSERACT_CONF_TEXTORD_NO_REJECTS}'
TESSERACT_LANG = r'slk+eng'


def get_data_from_ocr(documents):
    data = []
    for document in documents:
        data.append(pytesseract.image_to_data(
            image=document,
            lang=TESSERACT_LANG,
            config=TESSERACT_CONFIG,
            output_type=pytesseract.Output.DICT
        ))
        document.close()
    return data