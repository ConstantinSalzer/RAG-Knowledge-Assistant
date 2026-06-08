# Location: shared/schemas.py
from datetime import datetime
from typing import ClassVar, List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

class Chunk(BaseModel):
    file_name: str
    author: str
    confidence_score: float
    content: str


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
    llm: str = "Lokal"
    prompting_strategy: str = "Kreativ"

    MIN_TOP_K: ClassVar[int] = 1
    MAX_TOP_K: ClassVar[int] = 10

    LLM_OPTIONS: ClassVar[list[str]] = ["Lokal", "API"]
    PROMPT_STRATEGIES: ClassVar[list[str]] = ["Technisch", "Kreativ", "Defensiv"]
