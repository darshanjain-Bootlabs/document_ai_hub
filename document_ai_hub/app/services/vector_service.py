from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.documents import Document
from pathlib import Path

CHROMA_DIR = Path("/data/embeddings")
embeddings = HuggingFaceBgeEmbeddings(model_name = "all_miniLM_L6_v2")
vector_store = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)

def add_documents(documents: list[Document]):
    vector_store.add_documents(documents)
    vector_store.persist()

def similarity_search(query: str, k: int = 3) -> list[Document]:
    return vector_store.similarity_search(query, k=k)