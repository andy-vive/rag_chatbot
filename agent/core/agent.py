from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from agent.core.prompt import Prompt
from agent.memory import ConversationHistoryInMemory
from vectorstore.base import BaseVectorStore


class RAGAgent:
    def __init__(self, llm: BaseChatModel, embedding: Embeddings, vector_store: BaseVectorStore = None):
        self.llm = llm
        self.embedding = embedding
        self.vector_store = vector_store
        self.parser = StrOutputParser()
        self.conversation_history = ConversationHistoryInMemory()
        self.chain = None

        self._build_chain()

    async def chat(self, query: str, session_id: str) -> str:

        chain_input = {
            "user_query": query,
            "conversation_history": self._get_conversation_history(session_id),
            "context": await self._get_context(query)
        }

        self.conversation_history.add(session_id, "user", query)

        response = await self.chain.ainvoke(chain_input)

        self.conversation_history.add(session_id, "assistant", response)

        return response

    def _get_conversation_history(self, session_id: str) -> list:
        history = self.conversation_history.get(session_id)
        return Prompt.format_chat_history(history)

    async def _get_context(self, query: str, k: int = 5) -> str:
        if not self.vector_store:
            return ""
        
        try:
            relevant_docs = await self.vector_store.search(query, k=k)
            
            if not relevant_docs:
                return ""
            
            context_parts = []
            for i, doc in enumerate(relevant_docs, 1):
                context_parts.append(f"Document {i}:\n{doc.page_content}")
            
            return "\n\n".join(context_parts)
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return ""

    def _build_chain(self):
        self.chain = Prompt.get_prompt() | self.llm | self.parser
