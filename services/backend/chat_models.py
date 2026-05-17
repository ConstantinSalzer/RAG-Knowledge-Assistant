from pydantic import BaseModel
from typing import List
from services.backend.chunks import example_chunks, Chunk

from services.frontend.models.chat_settings import ChatSettings


class ChatRequest(BaseModel):
    message: str
    chat_settings: ChatSettings 


class ChatResponse(BaseModel):
    response: str
    chunks: List[Chunk]
