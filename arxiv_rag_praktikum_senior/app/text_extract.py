from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(Path(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
