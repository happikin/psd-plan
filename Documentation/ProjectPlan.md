# CoreHub Knowledge Analytics System
## Project Plan (Version 1.1 In-Flight)

---

# 1. Project Overview

The CoreHub Knowledge Analytics System delivers an MVP for ingestion, metadata extraction, analytics APIs, and graph/timeline data outputs.

Current phase: backend stabilization + storage migration prep + UI integration baseline.

---

# 2. Project Management Approach

The team follows a lightweight Scrum-inspired iterative approach:

- 2-week sprint cycles
- Sprint planning at the start of sprint
- Weekly progress sync
- Sprint review and retrospective
- GitLab issue tracking
- Feature branch workflow with merge requests

---

# 3. Team Structure and Role Allocation

| Role | Owners | Primary Responsibilities |
|------|----|--------------------------|
| Project Lead | Adam Todd | Planning, coordination, documentation oversight, risk management |
| Backend Lead | Yashesvi Raina | API development, ingestion pipeline, PostgreSQL migration |
| Data/NLP Lead | Hansheng Li | Metadata extraction quality, keyword/topic quality improvements |
| Frontend Lead | Xin Wen | UI implementation, graph/timeline visualisation, API integration |
| DevOps & QA Lead | Boyang Li | CI pipeline, test automation, release validation |

---

# 4. As-Built Progress Snapshot (2026-04-24)

Completed:
- FastAPI MVP endpoints for upload, listing/filtering, credibility, graph, timeline
- Dataset bootstrap from `Papers/` to `data/parsed/papers.jsonl`
- Deterministic metadata/keyword/reference/topic extraction pipeline
- API contract hardening: typed responses, standardized error schema, pagination metadata
- API contract documentation and automated contract tests

In progress:
- PostgreSQL replacement for in-memory repository (without API contract breakage)

Pending:
- Frontend implementation against `/documents`, `/documents/{paper_id}`, `/graph`, `/timeline`
- CI quality gates (tests, coverage, lint)
- Docker/deployment hardening

---

# 5. Work Breakdown Structure (Current)

## Workstream A - Backend/Data
- Migrate repository layer to PostgreSQL
- Add migration-safe regression tests
- Tune query/indexing performance

## Workstream B - Frontend
- Implement document list/detail views
- Integrate graph visualisation from `/graph`
- Integrate timeline view from `/timeline`

## Workstream C - QA/DevOps
- Add CI pipeline and coverage threshold
- Add lint/type checks
- Add performance benchmark script

## Workstream D - Documentation/Governance
- Keep API contract and traceability matrix synchronized with code
- Update risk and project artifacts each sprint

---

# 6. Milestone Alignment

## Milestone 1 (Completed)
- Requirements baseline established
- Initial architecture and risk baseline

## Milestone 2 (Completed)
- Working backend prototype with tests
- Dataset bootstrap and core analytics features

## Current Increment (In Progress)
- API contract finalized for UI consumption
- PostgreSQL migration with no public API shape change

## Final Submission (Planned)
- Stable deployable MVP with CI and deployment support
- Performance and usability evidence
- Complete synchronized documentation set

---

*End of Version 1.1 In-Flight Project Plan*
