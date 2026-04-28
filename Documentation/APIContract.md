# CoreHub API Contract

Last updated: 2026-04-28

This document defines the frontend-facing API contract for the backend in `src/backend/app.py`.

## Base

- Base URL: `http://127.0.0.1:8000`
- Content type: `application/json` unless noted
- API docs: `GET /docs` (Swagger UI)
- Contract source of truth: this file + generated OpenAPI schema (`GET /openapi.json`)

## Conventions

- `GET /documents` returns summary records (does not include `raw_text`).
- `GET /documents/{paper_id}` returns full detail (includes `raw_text`).
- Timeline is sparse by year (missing years are omitted).
- Graph values are stable enums:
  - `node.type`: `paper | author | keyword`
  - `edge.relationship`: `written_by | tagged_with | coauthor`
- Filtering semantics:
  - `author`: exact match, case-insensitive
  - `keyword`: exact match, case-insensitive
- Sorting semantics:
  - `sort_by=title`: case-insensitive lexical order
  - `sort_by=publication_date`: records with `null` year are always placed at the end
- Standard error envelope for all API errors:
  - `code` (machine-readable string)
  - `message` (human-readable summary)
  - `details` (optional object/list/string)
  - `request_id` (per-request identifier, also returned in `x-request-id` header)

## Persistence Model

- Runtime query state is persisted in a relational database via repository abstraction.
- Default DB URL (when `DATABASE_URL` is unset): `sqlite:///./data/corehub.db`.
- PostgreSQL is supported by setting `DATABASE_URL` (e.g. `postgresql+psycopg://...`).
- Parsed artifact cache (`data/parsed/papers.jsonl`) is an ingestion/bootstrap source, not the primary query store.
- Public API route signatures and response schemas are storage-engine agnostic.

## Error Schema

```json
{
  "code": "HTTP_404",
  "message": "Paper not found",
  "details": "Paper not found",
  "request_id": "1d9ac630-f14d-4324-8f7d-f7f2d4e4f9bb"
}
```

Validation error example:

```json
{
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "Request validation failed",
  "details": [
    {
      "loc": ["query", "keyword"],
      "msg": "String should have at least 2 characters",
      "type": "string_too_short"
    }
  ],
  "request_id": "1d9ac630-f14d-4324-8f7d-f7f2d4e4f9bb"
}
```

## Endpoints

### `GET /health`

Returns service liveness.

Response `200`:

```json
{
  "status": "ok"
}
```

### `POST /documents/upload`

Upload a PDF document.

- Request: `multipart/form-data`
- Required form field: `file` (PDF only)
- Allowed content types: `application/pdf`, `application/x-pdf`

Response `200`:

```json
{
  "paper_id": 1,
  "title": "Efficient Graph Mining",
  "authors": ["Alice Smith", "Bob Jones"],
  "keywords": ["graph mining", "citation analysis"],
  "topics": ["graph mining citation analysis"],
  "key_terms": ["graph", "mining", "citation"],
  "publication_date": 2022
}
```

Errors:

- `400` non-PDF upload
- `422` invalid/corrupt PDF parse

### `GET /documents`

Returns paginated paper summaries.

Query params:

- `author` (string, optional)
- `keyword` (string, optional)
- `year_from` (int, optional)
- `year_to` (int, optional)
- `page` (int, default `1`, min `1`)
- `page_size` (int, default `20`, min `1`, max `100`)
- `sort_by` (`uploaded_at | publication_date | title`, default `uploaded_at`)
- `sort_order` (`asc | desc`, default `desc`)

Response `200`:

```json
{
  "items": [
    {
      "id": 2,
      "title": "Applied NLP",
      "abstract": "Short abstract...",
      "publication_date": 2022,
      "sentiment": "positive",
      "uploaded_at": "2026-04-24T11:00:00Z",
      "authors": ["Alice"],
      "keywords": ["ai", "nlp"],
      "topics": ["language models"],
      "key_terms": ["nlp", "model"],
      "references": ["Paper A"]
    }
  ],
  "total": 43,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "has_next": true,
  "has_prev": false
}
```

Notes:

- `items[*]` intentionally excludes `raw_text`.
- When sorting by `publication_date`, records with `null` year are placed at the end.
- If `page` exceeds `total_pages`, response is `200` with empty `items`.

### `GET /documents/{paper_id}`

Returns full paper detail.

Path params:

- `paper_id` (int, required)

Response `200`:

```json
{
  "id": 2,
  "title": "Applied NLP",
  "raw_text": "Full parsed text...",
  "abstract": "Short abstract...",
  "publication_date": 2022,
  "sentiment": "positive",
  "uploaded_at": "2026-04-24T11:00:00Z",
  "authors": ["Alice"],
  "keywords": ["ai", "nlp"],
  "topics": ["language models"],
  "key_terms": ["nlp", "model"],
  "references": ["Paper A"]
}
```

Error:

- `404` paper not found (standard error schema)

### `GET /authors/credibility`

Returns author scores.

Response `200`:

```json
[
  {
    "id": 1,
    "name": "Alice",
    "credibility_score": 5
  }
]
```

### `GET /graph`

Returns graph payload for visualisation.

Response `200`:

```json
{
  "nodes": [
    { "id": "author:alice", "label": "Alice", "type": "author", "score": 5 },
    { "id": "paper:10", "label": "Applied NLP", "type": "paper", "score": null },
    { "id": "keyword:ai", "label": "ai", "type": "keyword", "score": null }
  ],
  "edges": [
    { "source": "author:alice", "target": "paper:10", "relationship": "written_by" },
    { "source": "paper:10", "target": "keyword:ai", "relationship": "tagged_with" },
    { "source": "author:alice", "target": "author:bob", "relationship": "coauthor" }
  ]
}
```

### `GET /timeline`

Returns yearly count for a keyword.

Query params:

- `keyword` (string, required, min length `2`)

Response `200`:

```json
[
  { "year": 2020, "count": 1 },
  { "year": 2022, "count": 3 }
]
```

Note: years with `0` count are not returned.

### `POST /admin/reset`

Dev/test helper. Clears persisted repository entities in the configured database.

Response `200`:

```json
{
  "status": "reset"
}
```

### `POST /admin/bootstrap-dataset`

Dev/test helper. Syncs `Papers/` to parsed dataset cache, resets database state, and reloads repository from parsed cache.

Query params:

- `force_reparse` (bool, default `false`)

Response `200`:

```json
{
  "loaded": 120,
  "parsed": 3,
  "failed": 0,
  "skipped": 117,
  "used_cache": false
}
```

Behavior notes:

- `force_reparse=true`: reparses all PDFs from `Papers/` into `data/parsed/papers.jsonl`, then reloads DB.
- `force_reparse=false`: appends only new PDFs (based on `source_file`) to parsed cache, then reloads DB.

## UI Integration Baseline

- Use `GET /documents` for list/table pages only.
- Use `GET /documents/{paper_id}` for detail panels/modals.
- Assume graph/timeline enums are stable and render by enum values, not free text.
- Do not call `/admin/*` from production UI flows.

## Non-Functional Baseline (Relaxed)

- Rate limit policy (soft): ~`600` requests/minute per client.
- Request payload policy (soft): recommend staying under `50MB` payload per request.
- Latency targets (best effort, not strict SLO):
  - `GET` endpoints: usually under `5s` on local/dev dataset.
  - PDF upload/parse: may exceed `5s` for large files.
- Quotas are advisory for now. Backend currently returns `x-soft-rate-limit-per-minute` and `x-soft-max-payload-mb` headers to communicate these limits.

## Internal Auth Scaffold

- Internal-only auth scaffolding exists in `src/backend/auth_scaffold.py`.
- It is intentionally not wired to middleware or route guards.
- There is no active user authentication requirement in the current API contract.
