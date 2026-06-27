from pathlib import Path

from pypdf import PdfReader


def clean_text(text: str) -> str:
    return text.replace("\x00", "")


def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(Path(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return clean_text(text)
