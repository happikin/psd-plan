# CoreHub Knowledge Analytics System
## Test Plan (Version 1.1 As-Built)

---

# 1. Testing Objectives

- Validate PDF ingestion and metadata extraction.
- Verify relational data integrity and credibility computation.
- Validate query, graph, and timeline correctness.
- Enforce API contract stability for UI development.
- Detect regressions during PostgreSQL migration.

---

# 2. Testing Levels

## Unit Testing
- Metadata extraction, keyword extraction, reference extraction
- Credibility scoring logic
- Query filtering logic
- Timeline aggregation logic

## Contract Testing
- Document list contract (`/documents`) including pagination metadata
- Document detail contract (`/documents/{paper_id}`)
- Stable graph node/edge enum values
- Standard API error envelope shape
- OpenAPI schema presence for response/error models

## Integration Testing
- Upload -> parse -> metadata -> repository -> credibility recomputation
- Dataset bootstrap -> load -> query flows

## System Testing (Planned)
- End-to-end UI + API workflows
- Deployment smoke tests

## Performance Testing (Planned)
- Soft target: typical GET APIs under ~5s on local/dev dataset
- Upload processing measured for large PDFs
- Benchmark script to be added (`T-011`)

---

# 3. Continuous Integration Status

Current state:
- Tests are runnable locally via `pytest`.
- Contract tests are available in `tests/test_api_contract.py`.

Pending (T-008):
- CI pipeline for automatic pytest on merge requests
- Coverage reporting and threshold gates
- Lint/type checks in CI

---

# 4. Current Test Artifacts

- `tests/test_services.py`
- `tests/test_dataset_service.py`
- `tests/test_api_contract.py`

---

*End of Version 1.1 As-Built Test Plan*
