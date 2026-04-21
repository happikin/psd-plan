from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from credibility_service import recompute_credibility
from dataset_service import bootstrap_repository
from graph_service import build_graph_payload
from metadata_extractor import extract_metadata
from models import IngestedDocument
from pdf_parser import PDFParserError, parse_pdf_text
from query_service import query_papers
from repository import InMemoryRepository
from timeline_service import keyword_timeline

app = FastAPI(title="CoreHub Knowledge Analytics System", version="0.1.0")
repo = InMemoryRepository()
papers_dir = Path("Papers")
parsed_dataset_path = Path("data/parsed/papers.jsonl")


@app.on_event("startup")
def startup_bootstrap() -> None:
    # Runtime loads parsed artifacts only; PDFs are used as a source for one-time parsing.
    bootstrap_repository(repo, papers_dir=papers_dir, parsed_output_path=parsed_dataset_path, force_reparse=False)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, object]:
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    file_bytes = await file.read()

    try:
        raw_text = parse_pdf_text(file_bytes)
    except PDFParserError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    metadata = extract_metadata(raw_text)
    paper = repo.add_document(
        IngestedDocument(
            title=metadata["title"],
            raw_text=raw_text,
            abstract=metadata["abstract"],
            publication_date=metadata["publication_date"],
            sentiment=metadata["sentiment"],
            authors=metadata["authors"],
            keywords=metadata["keywords"],
            references=metadata["references"],
        )
    )
    recompute_credibility(repo)

    return {
        "paper_id": paper.id,
        "title": paper.title,
        "authors": paper.authors,
        "keywords": paper.keywords,
        "publication_date": paper.publication_date,
    }


@app.get("/documents")
def list_documents(
    author: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
) -> list[dict[str, object]]:
    papers = query_papers(repo, author=author, keyword=keyword, year_from=year_from, year_to=year_to)
    return [paper.model_dump() for paper in papers]


@app.get("/authors/credibility")
def author_credibility() -> list[dict[str, object]]:
    recompute_credibility(repo)
    return [author.model_dump() for author in sorted(repo.all_authors(), key=lambda a: (-a.credibility_score, a.name.lower()))]


@app.get("/graph")
def graph() -> dict[str, object]:
    return build_graph_payload(repo).model_dump()


@app.get("/timeline")
def timeline(keyword: str = Query(..., min_length=2)) -> list[dict[str, int]]:
    return [point.model_dump() for point in keyword_timeline(repo, keyword)]


@app.post("/admin/reset")
def reset() -> dict[str, str]:
    repo.reset()
    return {"status": "reset"}


@app.post("/admin/bootstrap-dataset")
def bootstrap_dataset(force_reparse: bool = Query(default=False)) -> dict[str, int | bool]:
    return bootstrap_repository(
        repo,
        papers_dir=papers_dir,
        parsed_output_path=parsed_dataset_path,
        force_reparse=force_reparse,
    )
