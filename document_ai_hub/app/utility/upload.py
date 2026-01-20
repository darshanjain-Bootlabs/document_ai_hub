from fastapi import UploadFile, APIRouter, File
from app.common_utils.file_handler import save_file

upload_router = APIRouter()

@upload_router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    file_id  = save_file(file)
    return {"file": f"{file.filename}", "is successfully saved at": f"{file_id}"}