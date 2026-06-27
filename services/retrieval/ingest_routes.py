import hashlib
import tempfile
import time
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_session
from app.ingest import _ingest_paper
from app.models import Paper

router = APIRouter()


@router.post("/ingest")
def ingest_document(
    file: UploadFile = File(...),
    title: str = Form(default=""),
    author: str = Form(default="Unknown"),
    session: Session = Depends(get_session),
):
    filename = file.filename or "upload.pdf"
    file_bytes = file.file.read()

    uid = hashlib.sha256(f"{filename}{time.time()}".encode()).hexdigest()[:32]
    doc_title = title if title else Path(filename).stem

    suffix = Path(filename).suffix or ".pdf"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    paper = Paper(
        arxiv_id=uid,
        title=doc_title,
        abstract="",
        authors=author,
        published="",
        pdf_url="",
        pdf_path=tmp_path,
        score=0.0,
        fingerprint=uid,
        status="downloaded",
    )
    session.add(paper)
    session.flush()

    try:
        chunk_count = _ingest_paper(session, paper, batch_size=16)
        paper.status = "indexed"
        session.commit()
        return {"status": "ok", "chunks_stored": chunk_count}
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
