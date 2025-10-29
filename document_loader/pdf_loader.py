import hashlib
from datetime import datetime
from types import Dict

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)


class PDFLoader:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        splitter_type: str = "recursive",
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter_type = splitter_type

        self.text_splitter = self._get_text_splitter()

    def process_file(self, pdf_path: str) -> list[Dict]:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        chunks = self.text_splitter.split_documents(docs)

        documents = []
        for i, chunk in enumerate(chunks):
            doc_id = self._gen_doc_id(chunk, i)
            metadata = {
                "source": pdf_path,
                "filename": pdf_path,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "indexed_at": datetime.now().isoformat(),
                "loader_type": "pdf",
                **chunk.metadata,
            }

            documents.append({
                "id": doc_id,
                "content": chunk.page_content,
                "metadata": metadata,
            })

        return documents

    def process_directory(self, directory_path: str) -> str:
        pass

    def _get_text_splitter(self):
        """Get the appropriate text splitter"""
        if self.splitter_type == "recursive":
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
        elif self.splitter_type == "token":
            return TokenTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
        elif self.splitter_type == "character":
            return CharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separator="\n",
            )
        else:
            raise ValueError(f"Unknown splitter type: {self.splitter_type}")

    def _gen_doc_id(self, doc: Document, chunk_index: int) -> str:
        content = f"{doc.metadata.get('source', '')}__{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()
