from PIL import Image
import pytesseract
import easyocr
from pathlib import Path

_easyocr_reader = easyocr.Reader(['en'], gpu=False)

def extract_text_with_tesseract(image_path: Path) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_with_easyocr(image_path: Path) -> str:
    results = _easyocr_reader.readtext(str(image_path))
    return " ".join([text for (_, text, _) in results])