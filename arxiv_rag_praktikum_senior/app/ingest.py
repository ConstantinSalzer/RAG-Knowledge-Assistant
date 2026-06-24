import logging

from sqlalchemy.orm import Session

from app.chunking import chunk_text, token_estimate
from app.embedding import embed_texts
from app.models import Chunk, Paper
from app.text_extract import extract_pdf_text

logger = logging.getLogger(__name__)


def ingest_downloaded_papers(session: Session, batch_size: int = 16) -> int:
    papers = _papers_waiting_for_ingest(session)
    total_chunks = 0

    for paper in papers:
        try:
            chunk_count = _ingest_paper(session, paper, batch_size)
            paper.status = "indexed"
            total_chunks += chunk_count
            logger.info("Indexed %s with %s chunks", paper.arxiv_id, chunk_count)
        except Exception as exc:
            paper.status = "ingest_failed"
            logger.warning("Failed to ingest %s: %s", paper.arxiv_id, exc)

    session.commit()
    return total_chunks


def _papers_waiting_for_ingest(session: Session) -> list[Paper]:
    return (
        session.query(Paper)
        .filter(Paper.status == "downloaded")
        .order_by(Paper.created_at.asc())
        .all()
    )


def _ingest_paper(session: Session, paper: Paper, batch_size: int) -> int:
    text = extract_pdf_text(str(paper.pdf_path))
    chunks = chunk_text(text)
    embeddings = _embed_in_batches(chunks, batch_size)

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        session.add(
            Chunk(
                paper_id=paper.id,
                chunk_index=index,
                text=chunk,
                token_estimate=token_estimate(chunk),
                embedding=embedding,
            )
        )

    return len(chunks)


def _embed_in_batches(chunks: list[str], batch_size: int) -> list[list[float]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    embeddings: list[list[float]] = []

    for start in range(0, len(chunks), batch_size):
        embeddings.extend(embed_texts(chunks[start : start + batch_size]))

    return embeddings
