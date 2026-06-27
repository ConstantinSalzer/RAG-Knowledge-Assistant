import logging
from pathlib import Path

import arxiv
from sqlalchemy.orm import Session

from app.config import settings
from app.dedupe import paper_fingerprint
from app.models import Paper
from app.rate_limit import MinIntervalRateLimiter
from app.scoring import score_paper

logger = logging.getLogger(__name__)


def crawl_arxiv(session: Session, query: str, max_results: int = 25) -> int:
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    inserted = 0

    for result in client.results(search):
        arxiv_id = result.entry_id.rsplit("/", 1)[-1]
        title = result.title.strip()
        abstract = result.summary.strip()
        fingerprint = paper_fingerprint(title, abstract)

        if _paper_exists(session, arxiv_id, fingerprint):
            logger.info("Skipping duplicate paper %s", arxiv_id)
            continue

        paper = _build_paper(result, arxiv_id, title, abstract, fingerprint)
        session.add(paper)
        inserted += 1

    session.commit()
    logger.info("Inserted %s papers for query %r", inserted, query)
    return inserted


def download_accepted_pdfs(session: Session) -> int:
    download_dir = Path(settings.arxiv_download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    limiter = MinIntervalRateLimiter(settings.arxiv_download_delay_seconds)
    papers = _papers_waiting_for_download(session)

    downloaded = 0

    for paper in papers:
        limiter.wait()

        try:
            paper.pdf_path = str(_download_pdf(paper.arxiv_id, download_dir))
            paper.status = "downloaded"
            downloaded += 1
            logger.info("Downloaded %s", paper.arxiv_id)
        except Exception as exc:
            paper.status = "download_failed"
            logger.warning("Failed to download %s: %s", paper.arxiv_id, exc)

    session.commit()
    return downloaded


def _paper_exists(session: Session, arxiv_id: str, fingerprint: str) -> bool:
    return (
        session.query(Paper.id)
        .filter((Paper.arxiv_id == arxiv_id) | (Paper.fingerprint == fingerprint))
        .first()
        is not None
    )


def _build_paper(
    result: arxiv.Result,
    arxiv_id: str,
    title: str,
    abstract: str,
    fingerprint: str,
) -> Paper:
    score = score_paper(title, abstract)

    return Paper(
        arxiv_id=arxiv_id,
        title=title,
        abstract=abstract,
        authors=", ".join(author.name for author in result.authors),
        published=str(result.published.date()),
        pdf_url=result.pdf_url,
        score=score,
        fingerprint=fingerprint,
        status="accepted" if score >= settings.min_score else "filtered",
    )


def _papers_waiting_for_download(session: Session) -> list[Paper]:
    return (
        session.query(Paper)
        .filter(Paper.status == "accepted", Paper.pdf_path.is_(None))
        .order_by(Paper.created_at.asc())
        .all()
    )


def _download_pdf(arxiv_id: str, download_dir: Path) -> Path:
    search = arxiv.Search(id_list=[arxiv_id])
    result = next(arxiv.Client().results(search))

    file_path = download_dir / f"{arxiv_id.replace('/', '_')}.pdf"
    result.download_pdf(dirpath=str(download_dir), filename=file_path.name)

    return file_path
