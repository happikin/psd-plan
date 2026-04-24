# CoreHub Knowledge Analytics System
## Requirements Traceability Matrix (Version 1.2 As-Built)

---

| Requirement ID | Requirement Summary | Design Component | Implementation Module (As-Built) | Test Coverage Level | Status |
|----------------|--------------------|------------------|-----------------------------------|----------------------|--------|
| FR1.1 | PDF upload | Ingestion Module | `src/backend/app.py`, `src/backend/pdf_parser.py` | Unit + Integration | Implemented |
| FR2.1 | Store extracted raw text | Data Storage Layer | `src/backend/repository.py`, `src/backend/models.py`, `src/backend/dataset_service.py` | Unit + Integration | Implemented |
| FR2.3 | Relationship modelling | Data Model | `src/backend/relationship_service.py`, `src/backend/repository.py` | Unit | Implemented |
| FR3.1 | Extract document title | Metadata Extraction | `src/backend/metadata_extractor.py`, `src/backend/pdf_parser.py` | Unit | Implemented |
| FR3.3 | Extract author names | Metadata Extraction | `src/backend/metadata_extractor.py`, `src/backend/pdf_parser.py` | Unit | Implemented |
| FR3.4 | Extract/generate keywords and topics | Metadata & NLP | `src/backend/keyword_extractor.py`, `src/backend/topic_extractor.py`, `src/backend/metadata_extractor.py` | Unit | Implemented |
| FR3.5 | Extract references | Metadata Extraction | `src/backend/reference_extractor.py`, `src/backend/metadata_extractor.py` | Unit | Implemented |
| FR4.8 | Author credibility score | Analytics Engine | `src/backend/credibility_service.py` | Unit + Integration | Implemented |
| FR5.1 | Filter by author/keyword/year | Query Layer | `src/backend/query_service.py`, `src/backend/repository.py`, `src/backend/app.py` | Unit + Integration | Implemented |
| FR5.2 | Paginated/sorted document listing for UI | API Contract Layer | `src/backend/app.py`, `src/backend/models.py`, `Documentation/APIContract.md` | Contract + Unit | Implemented |
| FR5.3 | Document detail endpoint with full text | API Contract Layer | `src/backend/app.py`, `src/backend/models.py` | Contract + Unit | Implemented |
| FR6.6 | Graph-based view data | Graph Logic | `src/backend/graph_service.py`, `src/backend/models.py`, `src/backend/app.py` | Contract + Integration | Implemented (Backend) |
| FR6.8 | Keyword evolution timeline | Timeline Module | `src/backend/timeline_service.py`, `src/backend/app.py` | Unit + Integration | Implemented |
| FR7.2 | Stable API response/error schemas | API Governance | `src/backend/app.py`, `src/backend/models.py`, `Documentation/APIContract.md` | Contract + OpenAPI checks | Implemented |
| FR8.1 | Contract validation tests | QA/Verification | `tests/test_api_contract.py`, `tests/test_services.py`, `tests/test_dataset_service.py` | Automated Unit/Contract | Implemented |
| FR9.1 | Docker deployment | Deployment | `Dockerfile`, `docker-compose.yml` | System | Pending |
| FR9.2 | CI pipeline with quality gates | DevOps | CI configuration (TBD), pytest | Unit + Coverage + Lint | Pending |

---

*End of Version 1.2 As-Built Requirements Traceability Matrix*
