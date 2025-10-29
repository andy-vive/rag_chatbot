from vectorstore.base import BaseVectorStore
from vectorstore.chroma_db import ChromaDBVectorStore


class VectorStoreFactory:

    @staticmethod
    def create_vector_store(vector_store_type: str) -> BaseVectorStore:
        if vector_store_type == "chromadb":
            return ChromaDBVectorStore()
        else:
            raise ValueError(f"Unknown vector store type: {vector_store_type}")
