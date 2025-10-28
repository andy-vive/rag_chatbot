from abc import ABC, abstractmethod

from config import Setting


class BaseLLM(ABC):
    def __init__(self, setting: Setting):
        self.setting = setting

    @abstractmethod
    async def ainvoke(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass

    @abstractmethod
    async def generate_query_embedding(self, text: str) -> list[float]:
        pass
