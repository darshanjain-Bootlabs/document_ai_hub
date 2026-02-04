from fastapi import APIRouter, Depends, UploadFile, File, HTTPException,Request
from pathlib import Path
import tempfile
import shutil

from sqlalchemy.orm import Session

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.vector_service import inject_document
from app.common_utils.pdf_utils import text_from_pdf
from app.common_utils.txt_utils import text_from_txt
from app.services.ocr_service import extract_text
from app.services.whisper_service import text_from_audio
from app.utility.auth import get_current_user
from app.services.upload_service import create_doc
from app.utility.signup import get_db


upload_router = APIRouter(prefix="/upload", tags=["Upload"])
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg", ".wav", ".mp3", ".m4a"}

limiter = Limiter(key_func=get_remote_address)

@upload_router.post("/")
@limiter.limit("5/minutes")
async def upload_file(request: Request, file: UploadFile = File(...), file_domain: str = None, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    if suffix == ".pdf":
        text = text_from_pdf(await file.read())

    elif suffix == ".txt":
        text = text_from_txt(await file.read())

    elif suffix in [".png", ".jpg", ".jpeg"]:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(await file.read())
        try:
            text = extract_text(Path(tmp_path))
        finally:
            try:
                Path(tmp_path).unlink()
            except:
                pass

    elif suffix in [".wav", ".mp3", ".m4a"]:
        text = await text_from_audio(file)
    
    else:
        raise HTTPException(status_code=400, detail="File Handling Error")
    
    chunks = inject_document(text, file.filename, file_domain)

    try:
        create_doc(
            db,
            document_name=file.filename,
            file_domain=file_domain,
            uploaded_by=current_user["email"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database Error: " + str(e))
    return {"filename": file.filename, "file_domain": file_domain, "chunks_created": chunks}
