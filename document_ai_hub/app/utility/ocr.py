from PIL import Image
import pytesseract
import easyocr
from pathlib import Path

from fastapi import APIRouter,HTTPException
from app.services.ocr_services import extract_text

ocr_router = APIRouter()

@ocr_router.post("/extract")
def ocr_extract_text(file_id: str):
    file_path = Path(file_id)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        text = extract_text(file_path)
        return {"extracted_text is ": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


easyocr_reader = easyocr.Reader(['en'], gpu=False)

def extract_text_with_tesseract(image_path: Path) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_with_easyocr(image_path: Path) -> str:
    results = easyocr_reader.readtext(str(image_path))
    return " ".join([text for (_, text, _) in results])