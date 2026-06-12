# Location: shared/schemas.py
from datetime import datetime
from typing import ClassVar, List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

class Chunk(BaseModel):

    file_name: str                      # "machine_learning_basics.pdf"
    author: str                         # "John Doe"
    confidence_score: float             # 0.0 - 5.0
    content: str                        # "Machine learning is a subset of ..."

class Settings(BaseModel):
    max_tokens: int = Field(default=500, ge=1000, le=2000)       # 500
    role: str = "technical"                                     # "technical", "concise", "detailed"
    provider: str = "local"                                     # "local" (Ollama), "api" (Gemini API)
    mode: str = "fast"                                          # "fast", "complex"
    threshold: float = 4.0                                      # 4.0

class ChatRequest(BaseModel):

    query: str                                                  # "Was ist RAG?"
    settings: Settings = Field(default_factory=Settings)        # Optional settings with defaults

class SourceReference(BaseModel):

    file_name: str                  # "machine_learning_basics.pdf" or "Tavily Web Search"
    author: str                     # "John Doe"
    confidence_score: float         # 0.0 - 5.0

class ChatResponse(BaseModel):

    answer: str                                 # "RAG steht für ..."
    tokens_used: int                            # 450
    source_documents: List[SourceReference]     # [SourceReference(file_name="machine_learning_basics.pdf", author="John Doe", confidence_score=4.5)]
    aggregated_confidence: float                # 0.0 - 5.0


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: str
    chunks: Optional[List[Chunk]] = None


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


class ChatSettings(BaseModel):
    top_k: int = 5
    llm: str = "GPT-4"
    prompting_strategy: str = "Standard RAG"

    MIN_TOP_K: ClassVar[int] = 1
    MAX_TOP_K: ClassVar[int] = 20

    LLM_OPTIONS: ClassVar[list[str]] = ["GPT-4", "Llama 3", "Mistral"]
    PROMPT_STRATEGIES: ClassVar[list[str]] = ["Standard RAG", "Chain of Thought", "Concise"]
