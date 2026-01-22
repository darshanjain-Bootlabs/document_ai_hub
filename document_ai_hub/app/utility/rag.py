from fastapi import APIRouter
from app.services.rag_service import generate_answer
rag_router = APIRouter()    
@rag_router.post("/rag")

def rag_query(query: str, top_k: int = 3):
    return generate_answer(query, top_k=top_k)
