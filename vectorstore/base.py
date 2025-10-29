from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseVectorStore(ABC):

    @abstractmethod
    async def add_documents(self, documents: list[Document]):
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        pass

    @abstractmethod
    async def search_by_vector(
        self,
        embedding: list[float],
        k: int = 5,
    ) -> list[Document]:
        pass
