from fastapi import APIRouter
from app.utility.auth import auth_router
from app.utility.upload import upload_router
from app.utility.search import search_router
from app.utility.rag import rag_router
from app.utility.ocr import ocr_router
from app.utility.embedding import embedding_router

router = APIRouter()

router.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(search_router, prefix="/search", tags=["Search"])
router.include_router(rag_router, prefix="/rag", tags=["RAG"])
router.include_router(embedding_router, prefix="/embedding", tags=["Embedding"])