
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from config import Setting


class LLMFactory:

    @staticmethod
    def create(setting: Setting) -> Tuple[BaseChatModel, Embeddings]:
        if setting.llm_provider == "google":
            llm = ChatGoogleGenerativeAI(
                google_api_key=setting.google_api_key,
                model=setting.gemini_model,
                max_tokens=setting.max_tokens,
                temperature=0.7,
            )

            embedding = GoogleGenerativeAIEmbeddings(
                google_api_key=setting.google_api_key,
                model=setting.embedding_model,
            )

            return llm, embedding
        else:
            raise ValueError(f"Unknown LLM type: {setting.llm_provider}")
