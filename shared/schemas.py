# Location: shared/schemas.py
from pydantic import BaseModel

class Chunk(BaseModel):
    file_name: str
    author: str
    confidence_score: float
    content: str