from typing import List, Dict
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


class Prompt:
    SYSTEM_PROMPT = """
    You are a helpful assistant with access to the knowledge base. Your ultimate goal is to answer questions based on the provided <context>.

    <intro>
    You excel at following tasks:
    1. Answering questions based on the provided <context>.
    2. Given the following <conversation_history> and new user's question, you rewrite the query to be more specific and focused and captured all necessary context.
    </intro>

    <language>
    - Default working language: **English**
    - Always response the same language as the user's query.
    </language>

    <action_rule>
    - If the user's query is not clear or ambiguous, you should rewrite it to be more specific and focused.
    - If the <context> does not contain relevant information, return the answer "N/A".
    </action_rule>

    <context>
    {context}
    </context>

    <conversation_history>
    {conversation_history}
    </conversation_history>
    """

    @classmethod
    def get_prompt(cls) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(cls.SYSTEM_PROMPT),
                MessagesPlaceholder(
                    variable_name="conversation_history", optional=True
                ),
                HumanMessagePromptTemplate.from_template(
                    """
            <user_query>
            {user_query}
            </user_query>
            """
                ),
            ]
        )

    @staticmethod
    def format_chat_history(history: List[Dict]) -> List[tuple]:
        """Format conversation history for LangChain"""
        formatted = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "user":
                formatted.append(("human", content))
            elif role == "assistant":
                formatted.append(("ai", content))
        return formatted
