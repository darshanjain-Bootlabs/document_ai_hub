from fastapi import APIRouter
from app.services.rag_service import generate_answer
rag_router = APIRouter()    
@rag_router.post("/answer")
def rag_answer(query: str, file_id: str):
    answer = generate_answer(query, file_id)
    return {"answer": answer}