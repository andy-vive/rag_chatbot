from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from agent.core.prompt import Prompt
from agent.memory import ConversationHistoryInMemory


class RAGAgent:
    def __init__(self, llm: BaseChatModel, embedding: Embeddings):
        self.llm = llm
        self.embedding = embedding
        self.parser = StrOutputParser()
        self.conversation_history = ConversationHistoryInMemory()
        self.chain = None

        self._build_chain()

    async def chat(self, query: str, session_id: str) -> str:
        
        chain_input = {
            "user_query": query,
            "conversation_history": self._get_conversation_history(session_id),
            "context": self._get_context()
        }

        self.conversation_history.add(session_id, "user", query)

        response = await self.chain.ainvoke(chain_input)
        
        self.conversation_history.add(session_id, "assistant", response)

        return response

    def _get_conversation_history(self, session_id: str) -> list:
        history = self.conversation_history.get(session_id)
        return Prompt.format_chat_history(history)

    def _get_context(self) -> str:
        return ""

    def _build_chain(self):
        self.chain = Prompt.get_prompt() | self.llm | self.parser