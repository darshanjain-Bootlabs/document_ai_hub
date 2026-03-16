from fastapi import APIRouter, HTTPException, Depends, Request
from app.services.vector_service import VectorService
from app.utility.auth import get_current_user, require_role
from app.utility.api_key import verify_api_key

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
search_router = APIRouter()

vector_service = VectorService.create_default() 

@search_router.post("/search")
@limiter.limit("5/minute")
def semantic_search(request: Request, query: str, top_k: int = 3, user = Depends(require_role(["admin","researcher"])), client = Depends(verify_api_key)):
    try:
        docs = vector_service.similarity_search(query, k=top_k)
        return {
            "Client": client,
            "query": query,
            "results": [
                {"content": doc.page_content,
                  "metadata": doc.metadata }
                for doc in docs
                ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))