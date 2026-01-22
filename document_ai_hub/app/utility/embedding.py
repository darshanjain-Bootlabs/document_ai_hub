from fastapi import HTTPException, APIRouter
from app.services.vector_service import reset_vector_store, vector_store
from app.utility.text_splitter import split_text

embedding_router = APIRouter()

@embedding_router.post("/add")
async def generate_embeddings(text: str):
    try:
        documents = split_text(text)
        vector_store.add_documents(documents)

        return {"message": "Documents added successfully.",
                "chunks_added": len(documents)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
