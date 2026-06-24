import typer
from rich import print

from app.crawler import crawl_arxiv, download_accepted_pdfs
from app.db import SessionLocal, init_db
from app.ingest import ingest_downloaded_papers
from app.logging_config import configure_logging
from app.retrieval import vector_search

cli = typer.Typer(no_args_is_help=True)


@cli.callback()
def main() -> None:
    configure_logging()


@cli.command()
def init() -> None:
    init_db()
    print("[green]Database initialized[/green]")


@cli.command()
def crawl(query: str, max_results: int = 25) -> None:
    init_db()

    with SessionLocal() as session:
        count = crawl_arxiv(session, query, max_results)

    print(f"[green]Inserted {count} papers[/green]")


@cli.command()
def download() -> None:
    with SessionLocal() as session:
        count = download_accepted_pdfs(session)

    print(f"[green]Downloaded {count} PDFs[/green]")


@cli.command()
def ingest(batch_size: int = 16) -> None:
    with SessionLocal() as session:
        count = ingest_downloaded_papers(session, batch_size=batch_size)

    print(f"[green]Indexed {count} chunks[/green]")


@cli.command()
def search(query: str, limit: int = 5) -> None:
    with SessionLocal() as session:
        results = vector_search(session, query, limit)

    for result in results:
        print(result["title"])
        print(f"Similarity: {result['similarity']:.3f}")
        print(result["text"][:400])
        print("---")


if __name__ == "__main__":
    cli()
