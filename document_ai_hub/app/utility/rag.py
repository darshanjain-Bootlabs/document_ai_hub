from fastapi import APIRouter, Depends
from app.services.rag_service import generate_answer
from app.utility.auth import get_current_user
rag_router = APIRouter() 

@rag_router.post("/rag")
def rag_query(query: str, response_format: str, top_k: int = 3, user: dict = Depends(get_current_user)):
    return generate_answer(query, top_k=top_k, response_format=response_format)
