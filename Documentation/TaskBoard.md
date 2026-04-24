# CoreHub Task Board

Use this file as the shared internal task list for planning and execution.

## How we use this

- Add new tasks to `Backlog`.
- Move tasks to `In Progress` when work starts.
- Move tasks to `Done` when completed and verified.
- Keep task IDs stable (`T-001`, `T-002`, ...).
- Optional priority: `P1` (high), `P2` (medium), `P3` (low).

## Backlog

| ID | Priority | Task | Owner | Notes |
|----|----------|------|-------|-------|
| T-006 | P1 | Build React + D3 frontend consuming `/graph` and `/timeline` | Team | UI shell + graph interactions |
| T-007 | P1 | Replace in-memory repository with SQLite/PostgreSQL | Team | Persist parsed artifacts and queryable entities |
| T-008 | P1 | Add CI pipeline (pytest, coverage threshold, lint checks) | Team | Align with test plan and risk register |
| T-009 | P2 | Improve metadata extraction quality for noisy PDF layouts | Team | Parser heuristics + fallback paths |
| T-010 | P2 | Add retraction/reliability signal integration | Team | External source checks and API exposure |
| T-011 | P3 | Add performance benchmark script for query latency targets | Team | Validate relaxed NFR baseline and DB migration impact |
| T-014 | P2 | Replace FastAPI `on_event` startup with lifespan handler | Team | Remove deprecation warnings and stabilize startup contract |

## In Progress

| ID | Priority | Task | Owner | Started | Notes |
|----|----------|------|-------|---------|-------|
| T-007 | P1 | Replace in-memory repository with SQLite/PostgreSQL | Team | 2026-04-24 | Keep external API contract unchanged during storage migration |

## Done

| ID | Priority | Task | Owner | Completed | Evidence |
|----|----------|------|-------|-----------|----------|
| T-001 | P1 | Scaffold backend MVP with FastAPI modules | Team | 2026-04-21 | `src/app.py`, service modules, tests |
| T-002 | P1 | Implement credibility, query, graph, timeline services | Team | 2026-04-21 | `src/credibility_service.py`, `src/query_service.py`, `src/graph_service.py`, `src/timeline_service.py` |
| T-003 | P1 | Set up tests for extraction and analytics core flows | Team | 2026-04-21 | `tests/test_services.py` |
| T-004 | P1 | Migrate PDF parser to PyMuPDF | Team | 2026-04-21 | `src/pdf_parser.py`, `pyproject.toml`, `Documentation/TechnologyOptions.md` |
| T-005 | P1 | Add parsed dataset bootstrap from `Papers/` to `data/parsed/papers.jsonl` | Team | 2026-04-21 | `src/dataset_service.py`, startup bootstrap, `tests/test_dataset_service.py` |
| T-012 | P1 | Finalize UI-baseline API contract (summary/detail split, pagination, sorting, typed graph enums) | Team | 2026-04-24 | `src/backend/app.py`, `src/backend/models.py`, `tests/test_api_contract.py` |
| T-013 | P1 | Standardize API error schema and typed OpenAPI response models | Team | 2026-04-24 | `src/backend/app.py`, `src/backend/models.py`, `Documentation/APIContract.md` |

## Quick Add Template

Copy this row into `Backlog`:

`| T-XXX | P2 | <task description> | <owner> | <notes> |`
