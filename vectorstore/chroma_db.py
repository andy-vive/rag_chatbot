import asyncio
import uuid

import chromadb
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document

from config import setting

from .base import BaseVectorStore


class ChromaDB(BaseVectorStore):

    def __init__(self, embedding_function: Embeddings):
        super().__init__()
        self.persist_directory = setting.chroma_persist_directory
        self.collection_name = setting.chroma_collection_name
        self.client = None
        self.collection = None
        self.embedding_function = embedding_function

    async def add_documents(
        self,
        documents: list[dict],
        batch_size: int = 100,
    ):
        await self._get_or_create_collection()

        ids = []

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]

            batch_ids = [doc["id"] for doc in batch]
            batch_texts = [doc["content"] for doc in batch]
            batch_metadatas = [doc["metadata"] for doc in batch]

            embeddings = self.embedding_function.embed_documents(batch_texts)

            self.collection.add(
                ids=batch_ids,
                documents=batch_texts,
                metadatas=batch_metadatas,
                embeddings=embeddings,
            )
            ids.extend(batch_ids)

    async def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        await self._get_or_create_collection()
        
        query_embedding = self.embedding_function.embed_query(query)
        
        loop = asyncio.get_event_loop()
        
        def _search():
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            return results
        
        results = await loop.run_in_executor(None, _search)
        
        documents = []
        for i in range(len(results["documents"][0])):
            doc = Document(
                page_content=results["documents"][0][i],
                metadata=results["metadatas"][0][i] if results["metadatas"][0] else {}
            )
            documents.append(doc)
        
        return documents

    async def search_by_vector(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> list[Document]:
        await self._get_or_create_collection()
        
        loop = asyncio.get_event_loop()
        
        def _search():
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            return results
        
        results = await loop.run_in_executor(None, _search)
        
        documents = []
        for i in range(len(results["documents"][0])):
            doc = Document(
                page_content=results["documents"][0][i],
                metadata=results["metadatas"][0][i] if results["metadatas"][0] else {}
            )
            documents.append(doc)
        
        return documents

    async def _initialize(self):
        """Initialize ChromaDB client and collection"""
        loop = asyncio.get_event_loop()

        def _init():
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False),
            )

            try:
                self.collection = self.client.get_collection(self.collection_name)
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.collection_name, metadata={"hnsw:space": "cosine"}
                )

        await loop.run_in_executor(None, _init)

    async def _get_or_create_collection(self):
        if not self.collection:
            await self._initialize()
        return self.collection
