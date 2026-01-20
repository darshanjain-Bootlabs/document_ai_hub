from fastapi import APIRouter, HTTPException
from pathlib import Path
from app.services.ocr_service import extract_text

ocr_router = APIRouter()

@ocr_router.post("/extract")
def ocr_extract(file_id: str):
    documents_dir = Path("data/documents")
    matching_files = list(documents_dir.glob(f"{file_id}_*"))

    if not matching_files:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = matching_files[0]

    try:
        text = extract_text(file_path)
        return {"extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))