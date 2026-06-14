from datetime import datetime
from typing import List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

class Chunk(BaseModel):

    file_name: str                      # "machine_learning_basics.pdf"
    author: str                         # "John Doe"
    confidence_score: float             # 0.0 - 5.0
    content: str                        # "Machine learning is a subset of ..."

class Settings(BaseModel):
    max_tokens: int = Field(default=500, ge=1, le=2000)          # 500
    role: str = "technical"                                     # "technical", "concise", "detailed"
    provider: str = "local"                                     # "local" (Ollama), "api" (Gemini API)
    mode: str = "fast"                                          # "fast", "complex"
    threshold: float = 4.0                                      # 4.0

# Maximum number of previous messages (user+assistant) sent to /augment as conversation history
MAX_HISTORY_MESSAGES = 6

class SourceReference(BaseModel):

    file_name: str                  # "machine_learning_basics.pdf" or "Tavily Web Search"
    author: str                     # "John Doe"
    confidence_score: float         # 0.0 - 5.0

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: str
    chunks: Optional[List[SourceReference]] = None
    needs_confirmation: bool = False    # True if this assistant message is asking whether to search the web
    used_web_search: bool = False       # True if this assistant message's content came from a web search
    tokens_used: int = 0                # Token count of the LLM's response only (not context/prompt)

class ChatRequest(BaseModel):

    query: str                                                  # "Was ist RAG?"
    settings: Settings = Field(default_factory=Settings)        # Optional settings with defaults
    history: List[ChatMessage] = Field(default_factory=list)    # Previous turns of the conversation (most recent last)
    confirm_web_search: bool = False                            # User confirmed: search the web for this query

class ChatResponse(BaseModel):

    answer: str                                 # "RAG steht für ..."
    tokens_used: int                            # 450
    source_documents: List[SourceReference]     # [SourceReference(file_name="machine_learning_basics.pdf", author="John Doe", confidence_score=4.5)]
    aggregated_confidence: float                # 0.0 - 5.0
    needs_confirmation: bool = False            # True: nothing found in the knowledge base, ask the user whether to search the web
    used_web_search: bool = False               # True: this answer was generated using web search results


class ChatConversation(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[ChatMessage] = Field(default_factory=list)

    @classmethod
    def create_new(cls):
        now = datetime.now().isoformat(timespec="seconds")

        return cls(
            id=str(uuid4()),
            title="Neuer Chat",
            created_at=now,
            updated_at=now
        )
