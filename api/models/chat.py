
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    stream: bool = False
    session_id: str


class ChatResponse(BaseModel):
    response: str
    session_id: str
