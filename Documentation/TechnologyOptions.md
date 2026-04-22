# CoreHub Knowledge Analytics System
## Technology Options and Stack Decisions (Version 1.0)

---

# 1. Purpose

This document records the software stack used in the CoreHub MVP, why each option was selected, what alternatives were evaluated, and which components of the project are implemented with each technology.

---

# 2. Decision Principles

The stack was selected using these principles:

- Fast delivery for MVP milestone timelines.
- Strong maintainability for a student/team project.
- Good ecosystem support for analytics + API + graph visualisation.
- Clear testability and CI integration.
- Low operational complexity in early releases.

---

# 3. Technology Decisions

## 3.1 Backend API Framework

### Selected
- **FastAPI (Python)**

### Alternatives considered
- Flask (Python)
- Django + Django REST Framework (Python)
- Express (Node.js)

### Why FastAPI was selected
- Native support for type hints and request/response validation via Pydantic.
- Automatic OpenAPI/Swagger docs (`/docs`) which accelerates frontend integration and testing.
- Clean modular architecture for service-based design (ingestion, analytics, query, timeline).
- Good performance for I/O-bound API workloads in MVP scale.

### Why alternatives were not selected
- **Flask:** Very flexible but requires more manual setup for validation, schema docs, and larger API structure.
- **Django/DRF:** Powerful, but heavier than needed for a lean MVP and has steeper setup overhead for this scope.
- **Express:** Strong option, but team documentation and implementation are currently Python-first (NLP and ingestion pipeline alignment).

### Project components using FastAPI
- `src/backend/app.py`
- REST endpoints: upload, query/filter, credibility, graph payload, timeline

---

## 3.2 Programming Language for Core Logic

### Selected
- **Python 3.10+**

### Alternatives considered
- Node.js/TypeScript
- Java
- Go

### Why Python was selected
- Best fit for text processing and NLP-related tasks with mature libraries.
- Faster iteration speed for research/analysis prototypes.
- Direct compatibility with PDF parsing and analytics utilities used by the team.

### Why alternatives were not selected
- **Node.js/TypeScript:** Great for web APIs, but relatively weaker NLP/data-science ecosystem compared with Python.
- **Java:** Robust enterprise option but slower prototyping for this team and project timeline.
- **Go:** Strong performance but less convenient for rapid NLP-driven experimentation.

### Project components using Python
- All backend modules in `src/backend/`
- Data extraction, credibility scoring, query logic, timeline aggregation
- Test suite in `tests/`

---

## 3.3 API Server Runtime

### Selected
- **Uvicorn (ASGI server)**

### Alternatives considered
- Gunicorn (with Uvicorn workers)
- Hypercorn

### Why Uvicorn was selected
- Standard runtime pairing with FastAPI.
- Lightweight and easy to run in development.
- Supports reload mode for rapid local iteration.

### Why alternatives were not selected
- **Gunicorn + workers:** More suitable for production hardening phase than MVP baseline.
- **Hypercorn:** Capable but less commonly used in team examples and documentation.

### Project components using Uvicorn
- Local run command in `README.md`
- API hosting for `src/backend/app.py`

---

## 3.4 Data Validation and Schema Modelling

### Selected
- **Pydantic v2**

### Alternatives considered
- Marshmallow
- Dataclasses + manual validation

### Why Pydantic was selected
- Tight integration with FastAPI.
- Clear model definitions for papers, authors, graph nodes, and timeline points.
- Strong runtime validation to reduce malformed data issues (NFR reliability).

### Why alternatives were not selected
- **Marshmallow:** Good serializer ecosystem, but less seamless with FastAPI-first workflow.
- **Manual validation:** Higher defect risk and maintenance burden.

### Project components using Pydantic
- `src/backend/models.py`
- Request/response shape consistency in API handlers

---

## 3.5 PDF Ingestion

### Selected
- **PyMuPDF (fitz)**

### Alternatives considered
- pdfplumber
- pypdf

### Why PyMuPDF was selected
- Better extraction quality on complex and inconsistently formatted PDFs.
- Faster parsing performance for larger documents and multi-file ingestion sessions.
- Strong low-level control for future extensions (layout-aware extraction, bounding-box level analysis).

### Why alternatives were not selected
- **pdfplumber:** Strong for tabular and layout extraction, but slower for general-purpose full-document ingestion in this MVP.
- **pypdf:** Lightweight and simple, but extraction quality is weaker on scanned/complex layouts compared to PyMuPDF.

### Project components using PyMuPDF
- `src/backend/pdf_parser.py`
- `POST /documents/upload` pipeline in `src/backend/app.py`

---

## 3.6 Frontend Visualisation Stack (Planned/Active WIP)

### Selected direction
- **React + D3.js**

### Alternatives considered
- Vue + ECharts
- Plain D3 (without React)
- Cytoscape.js

### Why React + D3.js was selected
- React provides robust UI structure and state management for filters and query controls.
- D3 offers maximum flexibility for custom graph/timeline visualisations required by FR6.x.
- Strong community resources and component ecosystem.

### Why alternatives were not selected
- **Vue + ECharts:** Faster chart setup but less custom control for complex network behaviour.
- **Plain D3 only:** Powerful but harder to maintain as application complexity grows.
- **Cytoscape.js:** Good network graphs, but less unified for mixed custom visuals and broader UI needs.

### Project components using React + D3
- Planned `src/frontend/` interface shell.
- Consumption of `/graph` and `/timeline` endpoints.

---

## 3.7 Testing Framework

### Selected
- **Pytest**

### Alternatives considered
- unittest (stdlib)
- nose2

### Why Pytest was selected
- Fast, readable tests with minimal boilerplate.
- Strong fixture ecosystem for integration-style testing.
- Well-suited for CI execution and coverage tooling.

### Why alternatives were not selected
- **unittest:** Stable but more verbose and slower to scale for service-oriented tests.
- **nose2:** Less common and weaker team familiarity.

### Project components using Pytest
- `tests/test_services.py`
- CI-ready test command: `pytest -q`

---

## 3.8 Packaging and Dependency Management

### Selected
- **pyproject.toml (PEP 621) + pip editable install**

### Alternatives considered
- requirements.txt only
- Poetry
- Pipenv

### Why pyproject + pip was selected
- Standards-based project metadata.
- Easy setup for course/CI environments.
- Editable installs simplify local development and import paths.

### Why alternatives were not selected
- **requirements.txt only:** Works but lacks complete project metadata.
- **Poetry/Pipenv:** Useful tools but add workflow/tooling overhead for team alignment.

### Project components using this stack
- `pyproject.toml`
- Local env setup and dependency install workflow in `README.md`

---

# 4. Component-to-Stack Mapping Summary

| Project Component | Current Technology Stack |
|------------------|--------------------------|
| API layer | FastAPI + Uvicorn |
| Domain/data models | Pydantic |
| PDF ingestion | PyMuPDF (fitz) |
| Metadata/analytics services | Python modules (`src/backend/*.py`) |
| Query/filter service | Python + FastAPI endpoint layer |
| Credibility computation | Python service (`credibility_service.py`) |
| Timeline aggregation | Python service (`timeline_service.py`) |
| Graph payload generation | Python service (`graph_service.py`) |
| Automated testing | Pytest |
| Frontend visualisation (planned) | React + D3.js |

---

# 5. Revisit Triggers

Technology decisions should be revisited when:

- Dataset size growth causes query latency beyond NFR targets.
- PDF extraction quality is insufficient for varied document layouts.
- Frontend interaction complexity requires specialized graph tooling.
- Deployment/security requirements exceed current MVP architecture.

---

*End of Version 1.0 Technology Options Document*
