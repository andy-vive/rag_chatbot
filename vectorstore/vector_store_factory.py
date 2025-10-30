from vectorstore.base import BaseVectorStore
from vectorstore.chroma_db import ChromaDB


class VectorStoreFactory:

    @staticmethod
    def create(vector_store_type: str, **kwargs) -> BaseVectorStore:
        if vector_store_type == "chromadb":
            return ChromaDB(**kwargs)
        else:
            raise ValueError(f"Unknown vector store type: {vector_store_type}")
