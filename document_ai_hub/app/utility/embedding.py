from fastapi import HTTPException, APIRouter
from app.services.vector_service import add_documents
from app.utility.text_splitter import split_text

embedding_router = APIRouter()

@embedding_router.post("/add")
async def generate_embeddings(text: str):
    try:
        documents = split_text(text)
        add_documents.add_documents(documents)

        return {"message": "Documents added successfully.",
                "chunks_added": len(documents)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))