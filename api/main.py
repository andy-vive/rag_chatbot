import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from endpoints import document, chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from agent.core import LLMFactory, RAGAgent
from config import Setting
from vectorstore import VectorStoreFactory

agent, vector_store = None, None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent, vector_store

    setting = Setting()

    llm, embedding = LLMFactory.create(setting)
    agent = RAGAgent(llm, embedding)

    vector_store = VectorStoreFactory.create(
        setting.vector_store_type,
        embedding_function=embedding,
    )

    chat.agent = agent
    document.vector_store = vector_store

    yield


app = FastAPI(
    title="RAG Chatbot API with LangChain",
    description="RAG Chatbot with Multi-Provider LLM Support",
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(document.router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
