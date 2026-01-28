from fastapi import APIRouter, HTTPException, Depends
from app.services.vector_service import similarity_search
from app.utility.auth import get_current_user, require_role

search_router = APIRouter()

@search_router.post("/search")
def semantic_search(query: str, top_k: int = 3, user = Depends(require_role(["admin","researcher"]))):
    try:
        docs = similarity_search(query, top_k)
        return {
            "query": query,
            "results": [
                {"content": doc.page_content,
                  "metadata": doc.metadata }
                for doc in docs
                ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))