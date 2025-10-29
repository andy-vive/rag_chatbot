from collections import deque


class ConversationHistoryInMemory:
    def __init__(self):
        self.conversations: dict[str, deque] = {}

    def get(self, session_id: str) -> deque:
        if session_id not in self.conversations:
            self.conversations[session_id] = deque(maxlen=10)

        return self.conversations[session_id]

    def add(self, session_id: str, role: str, message: str):
        if session_id not in self.conversations:
            self.conversations[session_id] = deque(maxlen=10)

        self.conversations[session_id].append(
            {
                "role": role,
                "content": message,
            }
        )
