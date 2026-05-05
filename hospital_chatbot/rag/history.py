"""
rag/history.py - Conversation History Manager
==============================================
Maintains per-session chat history so the bot can answer
follow-up questions with context from previous turns.

Example:
  User:  "What is diabetes?"
  Bot:   "Diabetes is a condition where..."
  User:  "What department handles it?"  ← needs previous context
  Bot:   "The Endocrinology department handles diabetes..."  ✅

Without history, the bot wouldn't know "it" = diabetes.

History is stored in-memory (dict keyed by session_id).
For production, replace with Redis or a database.
"""

from collections import defaultdict
from typing import List, Dict


class ConversationHistory:
    def __init__(self, max_history: int = 10):
        """
        Args:
            max_history: Maximum turns to keep per session.
                         Older turns are dropped to control prompt size.
        """
        self.max_history = max_history
        # { session_id: [{"user": ..., "bot": ...}, ...] }
        self._store: Dict[str, List[Dict]] = defaultdict(list)

    def add(self, session_id: str, user_msg: str, bot_msg: str):
        """Store a completed conversation turn."""
        self._store[session_id].append({
            "user": user_msg,
            "bot": bot_msg
        })
        # Keep only the last N turns to avoid context overflow
        if len(self._store[session_id]) > self.max_history:
            self._store[session_id] = self._store[session_id][-self.max_history:]

    def get_history(self, session_id: str, last_n: int = 6) -> List[Dict]:
        """
        Get last N turns of conversation for a session.
        
        Args:
            session_id: Unique identifier for the user's session
            last_n:     How many recent turns to include in the prompt
        """
        history = self._store.get(session_id, [])
        return history[-last_n:]

    def clear(self, session_id: str):
        """Reset conversation history for a session."""
        self._store[session_id] = []

    def session_count(self) -> int:
        """Total number of active sessions."""
        return len(self._store)