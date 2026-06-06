from pydantic import BaseModel
from typing import List
from schemas import Chunk, ChatSettings



class ChatRequest(BaseModel):
    message: str
    chat_settings: ChatSettings 


class ChatResponse(BaseModel):
    response: str
    chunks: List[Chunk]
