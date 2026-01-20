from pathlib import Path
from app.utility.ocr import (
    extract_text_with_tesseract,
    extract_text_with_easyocr
)

SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg"]

def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix in SUPPORTED_IMAGE_TYPES:
        try:
            return extract_text_with_tesseract(file_path)
        except Exception:
            return extract_text_with_easyocr(file_path)

    raise ValueError("Unsupported file type for OCR")