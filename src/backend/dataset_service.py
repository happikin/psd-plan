from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from credibility_service import recompute_credibility
from metadata_extractor import extract_metadata
from models import IngestedDocument
from pdf_parser import PDFParserError, parse_pdf_content
from repository import Repository


def _pdf_paths(papers_dir: Path) -> list[Path]:
    return sorted([p for p in papers_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])


def _build_ingested_document(parsed_pdf: dict[str, object]) -> IngestedDocument:
    raw_text = str(parsed_pdf["raw_text"])
    metadata = extract_metadata(
        raw_text,
        pdf_title=parsed_pdf.get("pdf_title"),
        pdf_author=parsed_pdf.get("pdf_author"),
        layout_title=parsed_pdf.get("layout_title"),
        layout_authors=parsed_pdf.get("layout_authors"),
    )
    return IngestedDocument(
        title=metadata["title"],
        raw_text=raw_text,
        abstract=metadata["abstract"],
        publication_date=metadata["publication_date"],
        sentiment=metadata["sentiment"],
        authors=metadata["authors"],
        keywords=metadata["keywords"],
        topics=metadata["topics"],
        key_terms=metadata["key_terms"],
        references=metadata["references"],
    )


def parse_papers_to_jsonl(papers_dir: Path, parsed_output_path: Path) -> Tuple[int, int]:
    parsed_output_path.parent.mkdir(parents=True, exist_ok=True)

    ingested_count = 0
    failed_count = 0

    with parsed_output_path.open("w", encoding="utf-8") as handle:
        for pdf_path in _pdf_paths(papers_dir):
            try:
                parsed_pdf = parse_pdf_content(pdf_path.read_bytes())
                doc = _build_ingested_document(parsed_pdf)
                payload = doc.model_dump()
                payload["source_file"] = pdf_path.name
                handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
                ingested_count += 1
            except (PDFParserError, OSError, ValueError):
                failed_count += 1

    return ingested_count, failed_count


def _existing_source_files(parsed_output_path: Path) -> set[str]:
    if not parsed_output_path.exists():
        return set()

    source_files: set[str] = set()
    with parsed_output_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            content = line.strip()
            if not content:
                continue
            try:
                item = json.loads(content)
            except json.JSONDecodeError:
                continue
            source_file = item.get("source_file")
            if isinstance(source_file, str) and source_file:
                source_files.add(source_file)
    return source_files


def append_new_papers_to_jsonl(papers_dir: Path, parsed_output_path: Path) -> Tuple[int, int, int]:
    parsed_output_path.parent.mkdir(parents=True, exist_ok=True)

    existing_files = _existing_source_files(parsed_output_path)
    ingested_count = 0
    failed_count = 0
    skipped_count = 0

    with parsed_output_path.open("a", encoding="utf-8") as handle:
        for pdf_path in _pdf_paths(papers_dir):
            if pdf_path.name in existing_files:
                skipped_count += 1
                continue
            try:
                parsed_pdf = parse_pdf_content(pdf_path.read_bytes())
                doc = _build_ingested_document(parsed_pdf)
                payload = doc.model_dump()
                payload["source_file"] = pdf_path.name
                handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
                ingested_count += 1
            except (PDFParserError, OSError, ValueError):
                failed_count += 1

    return ingested_count, failed_count, skipped_count


def load_parsed_jsonl(repository: Repository, parsed_path: Path) -> int:
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
    repository: Repository,
    papers_dir: Path,
    parsed_output_path: Path,
    force_reparse: bool = False,
) -> dict[str, int | bool]:
    parsed = 0
    failed = 0
    skipped = 0
    used_cache = True

    if force_reparse:
        if not papers_dir.exists():
            return {"loaded": 0, "parsed": 0, "failed": 0, "skipped": 0, "used_cache": False}
        parsed, failed = parse_papers_to_jsonl(papers_dir, parsed_output_path)
        used_cache = False
    elif papers_dir.exists():
        parsed, failed, skipped = append_new_papers_to_jsonl(papers_dir, parsed_output_path)
        used_cache = parsed == 0 and failed == 0

    repository.reset()
    loaded = load_parsed_jsonl(repository, parsed_output_path)
    return {"loaded": loaded, "parsed": parsed, "failed": failed, "skipped": skipped, "used_cache": used_cache}
