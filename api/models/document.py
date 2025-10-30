
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: str
    status: str
    chunks_created: int
    metadata: dict
