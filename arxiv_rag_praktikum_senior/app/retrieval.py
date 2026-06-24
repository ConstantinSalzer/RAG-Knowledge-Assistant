from sqlalchemy import text
from sqlalchemy.orm import Session

from app.embedding import embed_query


def vector_search(session: Session, query: str, limit: int = 5) -> list[dict]:
    if not query.strip():
        raise ValueError("query must not be empty")

    if limit <= 0:
        raise ValueError("limit must be greater than zero")

    query_vector = embed_query(query)
    rows = session.execute(
        text(
            """
            SELECT
                c.id AS chunk_id,
                p.arxiv_id,
                p.title,
                p.authors,
                p.published,
                c.text,
                1 - (c.embedding <=> :query_vector) AS similarity
            FROM chunks c
            JOIN papers p ON p.id = c.paper_id
            ORDER BY c.embedding <=> :query_vector
            LIMIT :limit
            """
        ),
        {
            "query_vector": str(query_vector),
            "limit": limit,
        },
    ).mappings()

    return [dict(row) for row in rows]
