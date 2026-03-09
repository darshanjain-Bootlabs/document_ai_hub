import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

from app.utility.text_splitter import split_text

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"
# we only need to create the local directory when using an on-disk store
# remote servers (chroma container) handle their own persistence
if not os.environ.get("CHROMA_HOST"):
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# support two modes:
# * standalone local store (persist_directory)
# * remote Chroma server (host/port from environment)
chroma_host = os.environ.get("CHROMA_HOST")
chroma_port = os.environ.get("CHROMA_PORT")

vector_args: dict = {"embedding_function": embeddings}
if chroma_host:
    # connect to the remote service defined in docker-compose
    vector_args.update({
        "host": chroma_host,
        "port": int(chroma_port) if chroma_port else 8000,
    })
else:
    vector_args["persist_directory"] = str(CHROMA_DIR)

vector_store = Chroma(**vector_args)

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

def similarity_search(query: str, k: int = 3, file_domain: str | None = None) -> list[Document]:
    """Run a similarity search against the vector store.

    If ``file_domain`` is provided we add a metadata filter so that only
    documents uploaded with that domain are returned.  The RAG endpoint passes
    ``doc_domain`` but previously ignored it, which could cause the user to
    believe no files were found.
    """
    if file_domain:
        return vector_store.similarity_search(query, k=k, filter={"file_domain": file_domain})
    return vector_store.similarity_search(query, k=k)
