from fastapi import APIRouter, Depends
from app.services.rag_service import generate_answer
from app.utility.auth import get_current_user

from slowapi import Limiter
from app.core.rate_limiter import get_remote_email
from fastapi import Depends, Request

rag_router = APIRouter() 
limiter = Limiter(key_func=get_remote_email)

@rag_router.post("/rag")
@limiter.limit("3/minutes")
def rag_query(request: Request, query: str, response_format: str, doc_domain: str, user: dict = Depends(get_current_user),mode: str = "general"):
    return generate_answer(query, response_format=response_format, doc_domain=doc_domain.lower(), user_role=user['role'], mode=mode)