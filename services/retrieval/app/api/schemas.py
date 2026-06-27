from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=50)


class SearchResult(BaseModel):
    chunk_id: int
    arxiv_id: str
    title: str
    authors: str
    published: str
    text: str
    similarity: float
