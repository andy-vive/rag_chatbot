from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse

from agent.core.agent import RAGAgent

agent: RAGAgent | None = None


def get_agent():
    global agent
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    return agent


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = get_agent()

    if request.stream:
        pass

    response = await agent.chat(request.query, request.session_id)
    return ChatResponse(response=response, session_id=request.session_id)
