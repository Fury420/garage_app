from io import BytesIO
from typing import Union, List
from PIL import Image
from pdf2image import convert_from_bytes


PDF_TO_IMG_DPI = 300
PDF_TO_IMG_FMT = "png"


def preprocess_image(document: Union[Image, bytes]) -> Union[Image, None]:
    if isinstance(document, bytes):
        img = Image.open(BytesIO(document))
    else:
        img = document

    if img.mode != "RBG":
        img.convert("RGB")

    """
    # Convert to OpenCV for advanced processing
    open_cv_image = np.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # RGB to BGR

    # 1. Convert to grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # 2. Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)

    # 3. Apply sharpening filter to enhance text edges
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(blurred, -1, kernel)

    # 4. Thresholding to get black/white image
    # Try different thresholding methods
    _, thresh_binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. Optional: Morphological operations to clean up text
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh_binary, cv2.MORPH_CLOSE, kernel)

    # Convert back to PIL
    result_img = Image.fromarray(cleaned)
    """

    return img


def preprocess_pdf(document: bytes) -> Union[List[Image], None]:
    images = convert_from_bytes(
        pdf_file=document,
        dpi=PDF_TO_IMG_DPI,
        fmt=PDF_TO_IMG_FMT,
        use_pdftocairo=True
    )
    if not images:
        return None
    processed_images = []
    for image in images:
        processed_image = preprocess_image(image)
        if processed_image is None:
            for to_close_image in images:
                to_close_image.close()
            return None
        processed_images.append(processed_image)
    return processed_images


def preprocess_document(document: bytes, is_pdf: bool = True) -> Union[List[Image], None]:
    if is_pdf:
        return preprocess_pdf(document)
    return preprocess_image(document)