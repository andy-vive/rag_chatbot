from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from config.settings import Setting

from .base import BaseLLM


class GoogleLLM(BaseLLM):
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.client = ChatGoogleGenerativeAI(
            google_api_key=setting.google_api_key,
            model=setting.gemini_model,
        )
        self.embedding_client = GoogleGenerativeAIEmbeddings(
            google_api_key=setting.google_api_key,
            model=setting.embedding_model,
        )

    async def ainvoke(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        pass

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass

    async def generate_query_embedding(self, text: str) -> list[float]:
        pass
