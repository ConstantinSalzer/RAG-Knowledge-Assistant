import hashlib
import re

_WORD_SEPARATOR = re.compile(r"[^a-z0-9äöüß ]+")
_WHITESPACE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    value = value.lower()
    value = _WORD_SEPARATOR.sub(" ", value)
    return _WHITESPACE.sub(" ", value).strip()


def paper_fingerprint(title: str, abstract: str) -> str:
    normalized = normalize_text(f"{title} {abstract[:500]}")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
