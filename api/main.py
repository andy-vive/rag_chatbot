from contextlib import asynccontextmanager

from endpoints import chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from agent.core import LLMFactory, RAGAgent
from config import Setting

agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent

    setting = Setting()
    llm, embedding = LLMFactory.create(setting)
    agent = RAGAgent(llm, embedding)

    chat.agent = agent

    yield

app = FastAPI(
    title="RAG Chatbot API with LangChain",
    description="RAG Chatbot with Multi-Provider LLM Support",
    version="0.0.1",
    lifespan=lifespan
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

if __name__ == "__main__":
    run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
