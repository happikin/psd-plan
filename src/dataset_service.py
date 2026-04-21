from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from credibility_service import recompute_credibility
from metadata_extractor import extract_metadata
from models import IngestedDocument
from pdf_parser import PDFParserError, parse_pdf_text
from repository import InMemoryRepository


def _pdf_paths(papers_dir: Path) -> list[Path]:
    return sorted([p for p in papers_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])


def _build_ingested_document(raw_text: str) -> IngestedDocument:
    metadata = extract_metadata(raw_text)
    return IngestedDocument(
        title=metadata["title"],
        raw_text=raw_text,
        abstract=metadata["abstract"],
        publication_date=metadata["publication_date"],
        sentiment=metadata["sentiment"],
        authors=metadata["authors"],
        keywords=metadata["keywords"],
        references=metadata["references"],
    )


def parse_papers_to_jsonl(papers_dir: Path, parsed_output_path: Path) -> Tuple[int, int]:
    parsed_output_path.parent.mkdir(parents=True, exist_ok=True)

    ingested_count = 0
    failed_count = 0

    with parsed_output_path.open("w", encoding="utf-8") as handle:
        for pdf_path in _pdf_paths(papers_dir):
            try:
                raw_text = parse_pdf_text(pdf_path.read_bytes())
                doc = _build_ingested_document(raw_text)
                payload = doc.model_dump()
                payload["source_file"] = pdf_path.name
                handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
                ingested_count += 1
            except (PDFParserError, OSError, ValueError):
                failed_count += 1

    return ingested_count, failed_count


def load_parsed_jsonl(repository: InMemoryRepository, parsed_path: Path) -> int:
    if not parsed_path.exists():
        return 0

    loaded_count = 0
    with parsed_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            content = line.strip()
            if not content:
                continue
            item = json.loads(content)
            item.pop("source_file", None)
            repository.add_document(IngestedDocument(**item))
            loaded_count += 1

    recompute_credibility(repository)
    return loaded_count


def bootstrap_repository(
    repository: InMemoryRepository,
    papers_dir: Path,
    parsed_output_path: Path,
    force_reparse: bool = False,
) -> dict[str, int | bool]:
    parsed_exists = parsed_output_path.exists()

    if force_reparse or not parsed_exists:
        if not papers_dir.exists():
            return {"loaded": 0, "parsed": 0, "failed": 0, "used_cache": False}
        parsed, failed = parse_papers_to_jsonl(papers_dir, parsed_output_path)
        repository.reset()
        loaded = load_parsed_jsonl(repository, parsed_output_path)
        return {"loaded": loaded, "parsed": parsed, "failed": failed, "used_cache": False}

    repository.reset()
    loaded = load_parsed_jsonl(repository, parsed_output_path)
    return {"loaded": loaded, "parsed": 0, "failed": 0, "used_cache": True}

