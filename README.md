# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, LangChain, and Google Gemini.

## Features

- 📄 PDF document upload and processing
- 🔍 Vector-based document search with ChromaDB
- 💬 Conversational AI with context awareness
- 🚀 FastAPI REST API endpoints
- 🧠 Memory for conversation history

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run the application:**
   ```bash
   uv run python api/main.py
   ```

4. **Access the API:**
   - API docs: http://localhost:8000/docs
   - Upload documents: POST `/documents/upload`
   - Chat: POST `/chat`

## Tech Stack

- **Backend:** FastAPI, Python 3.11+
- **LLM:** Google Gemini (LangChain)
- **Vector Store:** ChromaDB
- **Document Processing:** PyPDF, PDFPlumber
