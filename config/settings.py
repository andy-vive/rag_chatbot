
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Setting(BaseSettings):
    google_api_key: str = os.getenv("GOOGLE_API_KEY")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY")
    redis_url: str = os.getenv("REDIS_URL")
    max_tokens: int = os.getenv("MAX_TOKENS")
    embedding_model: str = os.getenv("EMBEDDING_MODEL")
    gemini_model: str = os.getenv("GEMINI_MODEL")

setting = Setting()
