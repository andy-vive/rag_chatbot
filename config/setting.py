
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Setting(BaseSettings):
    llm_provider: str = os.getenv("LLM_PROVIDER")
    google_api_key: str = os.getenv("GOOGLE_API_KEY")
    redis_url: str = os.getenv("REDIS_URL")
    max_tokens: int = os.getenv("MAX_TOKENS")
    embedding_model: str = os.getenv("EMBEDDING_MODEL")
    gemini_model: str = os.getenv("GEMINI_MODEL")

    vector_store_type: str = os.getenv("VECTOR_STORE_TYPE")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = os.getenv("CHROMA_COLLECTION_NAME")

    class Config:
        env_file = ".env"

setting = Setting()
