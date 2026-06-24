def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    clean_text = " ".join(text.split())
    chunks: list[str] = []
    start = 0

    while start < len(clean_text):
        end = min(start + chunk_size, len(clean_text))
        chunk = clean_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(clean_text):
            break

        start = end - overlap

    return chunks


def token_estimate(text: str) -> int:
    return max(1, len(text) // 4)
