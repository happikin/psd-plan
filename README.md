# CoreHub Knowledge Analytics System (Paper Analysis App)

This repository now contains an executable MVP aligned with the project story and the documentation in `Documentation/`.

## What is implemented

- `FastAPI` backend for document ingestion and analytics APIs.
- PDF upload endpoint with text parsing and metadata extraction.
- Dataset bootstrap pipeline that parses `Papers/*.pdf` into `data/parsed/papers.jsonl`.
- Runtime startup loading from parsed artifacts (not from PDF binaries).
- Deterministic keyword, reference, and sentiment extraction.
- In-memory relational model for papers, authors, keywords, and references.
- Author credibility scoring based on citation references in the ingested dataset.
- Query/filter API (author, keyword, year range).
- Graph payload API for D3 frontend integration.
- Keyword timeline API for topic evolution view.
- Unit tests for metadata extraction, credibility scoring, and timeline aggregation.

## Repository structure

- `Documentation/`: project plan, requirements, design, risks, test plan, traceability, shared task board.
- `src/`: backend modules and services.
- `tests/`: pytest test suite.

## Task tracking

- Shared internal task list: `Documentation/TaskBoard.md`
- Add new work to `Backlog`, move active work to `In Progress`, and completed work to `Done`.

## Quick start

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
. .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .[dev]
```

3. Run the backend:

```bash
uvicorn app:app --reload --app-dir src
```

4. Open API docs:

- `http://127.0.0.1:8000/docs`

## API endpoints (MVP)

- `GET /health`
- `POST /documents/upload` (PDF upload)
- `GET /documents` (supports `author`, `keyword`, `year_from`, `year_to`)
- `GET /authors/credibility`
- `GET /graph`
- `GET /timeline?keyword=<topic>`
- `POST /admin/reset` (test/dev helper)
- `POST /admin/bootstrap-dataset?force_reparse=<bool>` (parse/reload `Papers/` dataset)

## Dataset handling policy

- `Papers/` is treated as source-only input for initial parsing.
- Parsed runtime dataset is stored as `data/parsed/papers.jsonl`.
- The app loads cached parsed data on startup; PDFs are only re-read when cache is missing or `force_reparse=true` is used.
- This supports the requirement to operate on parsed/metadata representations during runtime.

## Run tests

```bash
pytest -q
```

## Documentation mapping

The following planned modules from `Documentation/TraceabilityMatrix.md` are implemented:

- `pdf_parser.py`
- `relationship_service.py`
- `credibility_service.py`
- `query_service.py`
- `graph_service.py`
- `timeline_service.py`

## Suggested next development steps

1. Replace in-memory repository with SQLite/PostgreSQL (SQLModel or SQLAlchemy).
2. Add robust PDF metadata extraction (title/author/date) using parser fallbacks.
3. Implement retraction status checks from external reliability sources.
4. Build the React + D3 frontend consuming `/graph` and `/timeline`.
5. Add CI pipeline with linting, type-checking, tests, and coverage thresholds.
