from fastapi import APIRouter, HTTPException
from app.services.vector_service import search_documents

router = APIRouter()
@router.get("/similarity")
def semantic_search(query: str, top_k: int = 3):
    try:
        docs = search_documents(query, top_k)
        return {"results": [doc.page_content for doc in docs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))