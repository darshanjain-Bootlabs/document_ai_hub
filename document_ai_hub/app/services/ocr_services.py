from pathlib import Path
from document_ai_hub.app.utility.ocr import extract_text_with_tesseract, extract_text_with_easyocr

SUPPORTED_IMAGE_TYPES = {'.png', '.jpg', '.jpeg',}

def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in SUPPORTED_IMAGE_TYPES:
        return extract_text_with_easyocr(file_path)
    else:
        return "Unsupported file type for OCR extraction."