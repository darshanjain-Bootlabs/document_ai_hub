from fastapi import HTTPException, APIRouter
from app.services.vector_service import VectorService
from app.utility.text_splitter import split_text

embedding_router = APIRouter()
Vectorservice = VectorService.create_default()

@embedding_router.post("/add")
async def generate_embeddings(text: str):
    try:
        documents = split_text(text)
        Vectorservice.add_documents(documents)

        return {"message": "Documents added successfully.",
                "chunks_added": len(documents)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
