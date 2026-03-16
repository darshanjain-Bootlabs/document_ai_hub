import os
from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.utility.text_splitter import split_text


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"


class VectorService:

    def __init__(self, vector_store: Chroma):
        self.vector_store = vector_store

    @classmethod
    def create_default(cls):
        """
        Factory constructor for creating the vector store
        using environment configuration.
        """

        if not os.environ.get("CHROMA_HOST"):
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        chroma_host = os.environ.get("CHROMA_HOST")
        chroma_port = os.environ.get("CHROMA_PORT")

        vector_args: dict = {"embedding_function": embeddings}

        if chroma_host:
            vector_args.update({
                "host": chroma_host,
                "port": int(chroma_port) if chroma_port else 8000,
            })
        else:
            vector_args["persist_directory"] = str(CHROMA_DIR)

        vector_store = Chroma(**vector_args)

        return cls(vector_store)

    def inject_document(self, text: str, source: str, file_domain: str = None) -> int:

        if isinstance(text, list):
            text = "\n".join(text)

        chunks = split_text(text)

        documents: List[Document] = chunks

        for doc in documents:
            doc.metadata["source"] = source

            if file_domain:
                doc.metadata["file_domain"] = file_domain

        self.vector_store.add_documents(documents)

        return len(documents)

    def similarity_search(self, query: str, k: int = 3, file_domain: str | None = None) -> list[Document]:

        if file_domain:
            return self.vector_store.similarity_search(
                query,
                k=k,
                filter={"file_domain": file_domain}
            )

        return self.vector_store.similarity_search(query, k=k)