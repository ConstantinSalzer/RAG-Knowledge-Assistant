from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import SearchRequest
from app.db import get_session, init_db
from app.logging_config import configure_logging
from app.retrieval import vector_search

configure_logging()

app = FastAPI(title="arXiv RAG Retrieval API")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/search")
def search(req: SearchRequest, session: Session = Depends(get_session)) -> list[dict]:
    try:
        return vector_search(session, req.query, req.limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
