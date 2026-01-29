from fastapi import APIRouter, Depends
from app.services.rag_service import generate_answer
from app.utility.auth import get_current_user
rag_router = APIRouter() 

@rag_router.post("/rag")
def rag_query(query: str, response_format: str, doc_domain: str, user: dict = Depends(get_current_user),mode: str = "general"):
    return generate_answer(query, response_format=response_format, doc_domain=doc_domain.lower(), user_role=user['role'], mode=mode)