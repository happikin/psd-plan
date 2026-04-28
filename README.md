# CoreHub Knowledge Analytics System (Paper Analysis App)

This repository now contains an executable MVP aligned with the project story and the documentation in `Documentation/`.

## What is implemented

- `FastAPI` backend for document ingestion and analytics APIs.
- PDF upload endpoint with text parsing and metadata extraction.
- Dataset bootstrap pipeline that parses `Papers/*.pdf` into `data/parsed/papers.jsonl`.
- Runtime startup sync that parses only new PDFs and appends them to parsed artifacts.
- Deterministic keyword, reference, and sentiment extraction.
- Relational storage layer via SQLAlchemy repository.
- Default runtime DB is SQLite (`data/corehub.db`); PostgreSQL is supported via `DATABASE_URL`.
- Author credibility scoring based on citation references in the ingested dataset.
- Query/filter API (author, keyword, year range).
- Graph payload API for D3 frontend integration.
- Keyword timeline API for topic evolution view.
- Unit tests for metadata extraction, credibility scoring, and timeline aggregation.
- API contract tests for response models, pagination metadata, and error schema.

## Repository structure

- `Documentation/`: project plan, requirements, design, risks, test plan, traceability, API contract, shared task board.
- `src/backend/`: FastAPI backend modules and services.
- `src/frontend/`: frontend workspace placeholder for UI implementation.
- `tests/`: pytest test suite.

## Task tracking

- Shared internal task list: `Documentation/TaskBoard.md`
- API contract reference: `Documentation/APIContract.md`
- Add new work to `Backlog`, move active work to `In Progress`, and completed work to `Done`.

## Quick start

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .[dev]
```

3. Run the backend:

```bash
uvicorn app:app --reload --app-dir src/backend
```

Optional: run against PostgreSQL instead of default SQLite:

```bash
export DATABASE_URL='postgresql+psycopg://<user>:<pass>@<host>:<port>/<db>'
uvicorn app:app --reload --app-dir src/backend
```

4. Open API docs:

- `http://127.0.0.1:8000/docs`

## API endpoints (MVP)

- `GET /health`
- `POST /documents/upload` (PDF upload)
- `GET /documents` (paginated summary list; supports `author`, `keyword`, `year_from`, `year_to`, `page`, `page_size`, `sort_by`, `sort_order`)
- `GET /documents/{paper_id}` (full paper detail payload)
- `GET /authors/credibility`
- `GET /graph` (`node.type`: `paper|author|keyword`; `edge.relationship`: `written_by|tagged_with|coauthor`)
- `GET /timeline?keyword=<topic>` (sparse yearly counts; missing years are omitted)
- `POST /admin/reset` (test/dev helper)
- `POST /admin/bootstrap-dataset?force_reparse=<bool>` (parse/reload `Papers/` dataset)

## Dataset handling policy

- `Papers/` is treated as source-only input for initial parsing.
- Parsed ingestion cache is stored as `data/parsed/papers.jsonl`.
- Runtime query state is persisted in relational DB (`sqlite:///./data/corehub.db` by default, or `DATABASE_URL` if provided).
- On each startup, the app checks `Papers/` for files not already present in parsed cache and parses only those new PDFs.
- New parsed records are appended to `data/parsed/papers.jsonl`; existing parsed records are reused.
- Startup bootstrap then resets and reloads the DB state from the parsed cache.
- This supports the requirement to operate on parsed/metadata representations while using persistent relational storage.

## Parsed dataset schema (`data/parsed/papers.jsonl`)

Each JSONL entry stores:

- `title`
- `raw_text`
- `abstract`
- `publication_date`
- `sentiment`
- `authors`
- `keywords`
- `topics`
- `key_terms`
- `references`
- `source_file`

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

1. Add DB migration/versioning tooling (e.g. Alembic) instead of runtime `create_all`.
2. Add SQLite/PostgreSQL integration tests for persistence, constraints, and restart behavior.
3. Add robust PDF metadata extraction (title/author/date) using parser fallbacks.
4. Implement retraction status checks from external reliability sources.
5. Build the React + D3 frontend consuming `/graph` and `/timeline`.
