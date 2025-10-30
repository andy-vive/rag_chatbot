import os
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from models.document import DocumentResponse
from vectorstore.base import BaseVectorStore
from document_loader.pdf_loader import PDFLoader

vector_store: BaseVectorStore | None = None


def get_vector_store():
    global vector_store
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    return vector_store


router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile,
):
    """
    Upload and process a document using LangChain loaders

    Args:
        file: File to upload
    """
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(file.filename).suffix
    )
    try:
        shutil.copyfileobj(file.file, temp_file)
        temp_file.close()

        processor = PDFLoader()

        documents = processor.process_file(temp_file.name)

        if not documents:
            raise HTTPException(
                status_code=400, detail="Failed to extract content from file"
            )

        vector_store_instance = get_vector_store()
        doc_ids = await vector_store_instance.add_documents(documents)

        return DocumentResponse(
            document_id=doc_ids[0] if doc_ids else "unknown",
            status="processed",
            chunks_created=len(documents),
            metadata={
                "filename": file.filename,
                "size": file.size,
            },
        )
    finally:
        os.unlink(temp_file.name)
