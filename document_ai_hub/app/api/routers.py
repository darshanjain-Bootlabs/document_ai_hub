from fastapi import APIRouter
from document_ai_hub.app.utility.auth import auth_router
from document_ai_hub.app.utility.upload import upload_router
from document_ai_hub.app.utility.search import search_router
from document_ai_hub.app.utility.rag import rag_router
router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(search_router, prefix="/search", tags=["Search"])
router.include_router(rag_router, prefix="/rag", tags=["RAG"])