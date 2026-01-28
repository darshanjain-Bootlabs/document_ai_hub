from pathlib import Path
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

from app.utility.text_splitter import split_text

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings,
)
def reset_vector_store():
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    global vector_store
    vector_store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

def inject_document(text: str, source: str, file_domain: str = None) ->int:
    if isinstance(text, list):
        text = "\n".join(text)

    chunks = split_text(text)
    documents: List[Document] = chunks

    for doc in documents:
        doc.metadata["source"] = source
        if file_domain:
            doc.metadata["file_domain"] = file_domain

    vector_store.add_documents(documents)
    return len(documents)

def similarity_search(query: str, k: int = 3) -> list[Document]:
    return vector_store.similarity_search(query, k=k)
