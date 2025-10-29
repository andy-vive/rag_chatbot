from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

class RAGAgent:
    def __init__(self, llm: BaseChatModel, embedding: Embeddings):
        self.llm = llm
        self.embedding = embedding

    async def chat(self, query: str, session_id: str) -> str:
        return ""
