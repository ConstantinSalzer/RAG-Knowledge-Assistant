import pytest

from app.chunking import chunk_text


def test_chunk_text_returns_multiple_chunks():
    chunks = chunk_text("hello " * 1000, chunk_size=100, overlap=10)

    assert len(chunks) > 1


def test_chunk_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=10, overlap=10)
