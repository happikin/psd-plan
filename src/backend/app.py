from __future__ import annotations

import math
import uuid
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from credibility_service import recompute_credibility
from dataset_service import bootstrap_repository
from graph_service import build_graph_payload
from metadata_extractor import extract_metadata
from models import (
    APIErrorResponse,
    Author,
    BootstrapResponse,
    DocumentListResponse,
    DocumentUploadResponse,
    GraphPayload,
    HealthResponse,
    IngestedDocument,
    Paper,
    PaperSummary,
    ResetResponse,
    TimelinePoint,
)
from pdf_parser import PDFParserError, parse_pdf_content
from query_service import query_papers
from repository import create_repository
from timeline_service import keyword_timeline

app = FastAPI(title="CoreHub Knowledge Analytics System", version="0.1.0")
repo = create_repository()
papers_dir = Path("Papers")
parsed_dataset_path = Path("data/parsed/papers.jsonl")
SOFT_RATE_LIMIT_PER_MINUTE = 600
SOFT_MAX_PAYLOAD_MB = 50


@app.on_event("startup")
def startup_bootstrap() -> None:
    repo.ping()
    # On every boot, sync only new PDFs from Papers/ into parsed artifacts, then load runtime repository.
    bootstrap_repository(repo, papers_dir=papers_dir, parsed_output_path=parsed_dataset_path, force_reparse=False)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-soft-rate-limit-per-minute"] = str(SOFT_RATE_LIMIT_PER_MINUTE)
    response.headers["x-soft-max-payload-mb"] = str(SOFT_MAX_PAYLOAD_MB)
    return response


def _error_payload(code: str, message: str, details: object, request_id: str) -> dict[str, object]:
    return APIErrorResponse(code=code, message=message, details=details, request_id=request_id).model_dump()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    detail = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    code = f"HTTP_{exc.status_code}"
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(code=code, message=detail, details=exc.detail, request_id=request_id),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=422,
        content=_error_payload(
            code="REQUEST_VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
            request_id=request_id,
        ),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


def _paper_summary_payload(paper: Paper) -> PaperSummary:
    payload = paper.model_dump()
    payload.pop("raw_text", None)
    return PaperSummary(**payload)


def _sort_documents(
    papers: list[Paper],
    sort_by: Literal["uploaded_at", "publication_date", "title"],
    sort_order: Literal["asc", "desc"],
) -> list[Paper]:
    reverse = sort_order == "desc"

    if sort_by == "title":
        return sorted(papers, key=lambda p: p.title.lower(), reverse=reverse)
    if sort_by == "publication_date":
        # Keep records with missing years at the end regardless of direction.
        return sorted(
            papers,
            key=lambda p: (
                p.publication_date is None,
                p.publication_date if p.publication_date is not None else 0,
                p.title.lower(),
            ),
            reverse=reverse,
        )
    return sorted(papers, key=lambda p: p.uploaded_at, reverse=reverse)


@app.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
    responses={400: {"model": APIErrorResponse}, 422: {"model": APIErrorResponse}},
)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    file_bytes = await file.read()

    try:
        parsed = parse_pdf_content(file_bytes)
    except PDFParserError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    metadata = extract_metadata(
        parsed["raw_text"],
        pdf_title=parsed.get("pdf_title"),
        pdf_author=parsed.get("pdf_author"),
        layout_title=parsed.get("layout_title"),
        layout_authors=parsed.get("layout_authors"),
    )
    paper = repo.add_document(
        IngestedDocument(
            title=metadata["title"],
            raw_text=parsed["raw_text"],
            abstract=metadata["abstract"],
            publication_date=metadata["publication_date"],
            sentiment=metadata["sentiment"],
            authors=metadata["authors"],
            keywords=metadata["keywords"],
            topics=metadata["topics"],
            key_terms=metadata["key_terms"],
            references=metadata["references"],
        )
    )
    recompute_credibility(repo)

    return DocumentUploadResponse(
        paper_id=paper.id,
        title=paper.title,
        authors=paper.authors,
        keywords=paper.keywords,
        topics=paper.topics,
        key_terms=paper.key_terms,
        publication_date=paper.publication_date,
    )


@app.get("/documents", response_model=DocumentListResponse)
def list_documents(
    author: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: Literal["uploaded_at", "publication_date", "title"] = Query(default="uploaded_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
) -> DocumentListResponse:
    papers = query_papers(repo, author=author, keyword=keyword, year_from=year_from, year_to=year_to)
    sorted_papers = _sort_documents(papers, sort_by=sort_by, sort_order=sort_order)

    total = len(sorted_papers)
    total_pages = max(1, math.ceil(total / page_size)) if total else 1
    start = (page - 1) * page_size
    end = start + page_size
    items = [_paper_summary_payload(paper) for paper in sorted_papers[start:end]]

    return DocumentListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )


@app.get("/documents/{paper_id}", response_model=Paper, responses={404: {"model": APIErrorResponse}})
def document_detail(paper_id: int) -> Paper:
    paper = repo.get_paper(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.get("/authors/credibility", response_model=list[Author])
def author_credibility() -> list[Author]:
    recompute_credibility(repo)
    return sorted(repo.all_authors(), key=lambda a: (-a.credibility_score, a.name.lower()))


@app.get("/graph", response_model=GraphPayload)
def graph() -> GraphPayload:
    return build_graph_payload(repo)


@app.get("/timeline", response_model=list[TimelinePoint], responses={422: {"model": APIErrorResponse}})
def timeline(keyword: str = Query(..., min_length=2)) -> list[TimelinePoint]:
    return keyword_timeline(repo, keyword)


@app.post("/admin/reset", response_model=ResetResponse)
def reset() -> ResetResponse:
    repo.reset()
    return ResetResponse(status="reset")


@app.post("/admin/bootstrap-dataset", response_model=BootstrapResponse)
def bootstrap_dataset(force_reparse: bool = Query(default=False)) -> BootstrapResponse:
    result = bootstrap_repository(
        repo,
        papers_dir=papers_dir,
        parsed_output_path=parsed_dataset_path,
        force_reparse=force_reparse,
    )
    return BootstrapResponse(**result)
