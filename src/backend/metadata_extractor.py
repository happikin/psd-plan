from __future__ import annotations

import re
from typing import Dict, List, Optional

from keyword_extractor import extract_keywords
from reference_extractor import extract_references

POSITIVE_WORDS = {"reliable", "robust", "accurate", "effective", "improved", "strong", "significant"}
NEGATIVE_WORDS = {"bias", "weak", "error", "noise", "failed", "limited", "unstable"}


def _extract_title(lines: List[str]) -> str:
    for line in lines:
        if len(line.strip()) > 8:
            return line.strip()
    return "Untitled Document"


def _extract_authors(lines: List[str]) -> List[str]:
    if len(lines) < 2:
        return []
    candidate = lines[1]
    if len(candidate) > 140:
        return []
    parts = re.split(r",| and ", candidate)
    names = [p.strip() for p in parts if p.strip()]
    if any(char.isdigit() for char in candidate):
        return []
    return names[:8]


def _extract_abstract(text: str) -> str:
    match = re.search(r"\babstract\b[:\s]*(.+?)(\n\s*\n|\n\s*[A-Z][A-Za-z\s]{2,25}:?)", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return " ".join(match.group(1).split())[:2000]

    # Fallback for malformed files: use first paragraph chunk.
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) >= 2:
        return paragraphs[1][:1500]
    if paragraphs:
        return paragraphs[0][:1500]
    return ""


def _extract_publication_year(text: str) -> Optional[int]:
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if not years:
        return None
    for y in years:
        year = int(y)
        if 1990 <= year <= 2100:
            return year
    return int(years[0])


def _extract_explicit_keywords(text: str) -> List[str]:
    match = re.search(r"\bkeywords?\b\s*[:\-]\s*(.+)", text, flags=re.IGNORECASE)
    if not match:
        return []
    raw = match.group(1)
    parts = re.split(r",|;", raw)
    return [p.strip().lower() for p in parts if p.strip()][:12]


def detect_sentiment(text: str) -> str:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def extract_metadata(raw_text: str) -> Dict[str, object]:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    title = _extract_title(lines)
    authors = _extract_authors(lines)
    abstract = _extract_abstract(raw_text)
    publication_year = _extract_publication_year(raw_text)

    explicit_keywords = _extract_explicit_keywords(raw_text)
    auto_keywords = extract_keywords((abstract or raw_text)[:12000])
    keywords = list(dict.fromkeys(explicit_keywords + auto_keywords))[:12]

    references = extract_references(raw_text)

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "publication_date": publication_year,
        "keywords": keywords,
        "references": references,
        "sentiment": detect_sentiment(raw_text),
    }

