# CoreHub Knowledge Analytics System
## Risk Register (Version 1.1 As-Built)

---

# 1. Risk Management Methodology

Risks are assessed using a quantitative scoring model:

- Probability (P): Rated 1-5
- Impact (I): Rated 1-5
- Risk Score = P x I

Risk Levels:
- Low: 1-6
- Medium: 7-14
- High: 15-25

Risks are reviewed at the end of each sprint and updated accordingly.

---

# 2. Risk Register Table

| ID | Risk Description | Category | P | I | Score | Level | Mitigation Strategy | Owner | Status |
|----|------------------|----------|---|---|-------|-------|---------------------|--------|--------|
| R1 | PDF parsing inconsistencies due to layout variability | Technical | 3 | 4 | 12 | Medium | Keep heuristic extraction + expand parser edge-case tests | Backend Lead | Mitigated (Monitoring) |
| R2 | Scope creep due to large number of analytical features | Project | 4 | 3 | 12 | Medium | Keep P1 API+storage scope frozen during PostgreSQL migration | Project Lead | Open |
| R3 | NLP complexity exceeding team expertise | Technical | 2 | 3 | 6 | Low | Continue deterministic NLP pipeline and avoid model-heavy redesign in MVP | Data Lead | Mitigated (Monitoring) |
| R4 | Uneven workload distribution across team | Organisational | 3 | 4 | 12 | Medium | Parallelize by workstream (DB migration, UI, QA, docs) with clear ownership | Project Lead | Open |
| R5 | Performance degradation with increasing dataset size | Technical | 3 | 4 | 12 | Medium | Add benchmark script and DB indexing as part of PostgreSQL migration | Backend Lead | Open |
| R6 | Failure to meet deployment requirements | Operational | 2 | 4 | 8 | Medium | Add CI and containerization tasks before final release | DevOps Lead | Open |
| R7 | Insufficient automated testing coverage | Quality | 2 | 4 | 8 | Medium | Keep contract/unit tests in repo; enforce coverage and lint in CI (pending) | QA Lead | Reduced (Monitoring) |
| R8 | Data integrity issues during pipeline updates | Technical | 2 | 4 | 8 | Medium | Preserve parsed JSONL artifacts; add migration verification tests | Backend Lead | Mitigated (Monitoring) |
| R9 | Delays due to milestone feedback requiring redesign | Project | 3 | 3 | 9 | Medium | Keep API contract documented and stabilized to limit rework | Project Lead | Open |
| R10 | API contract drift between code and docs | Quality | 2 | 3 | 6 | Low | Maintain `Documentation/APIContract.md` + contract tests + OpenAPI checks | Backend/QA Leads | Mitigated (Monitoring) |
| R11 | Breaking changes introduced during PostgreSQL migration | Technical | 3 | 4 | 12 | Medium | Preserve route signatures/response schemas; regression test API contract after migration | Backend Lead | Open |

---

# 3. Risk Review Process

- Risks are reviewed at sprint review meetings.
- Scores are updated when mitigation status changes.
- Closed or mitigated risks are retained for traceability.
- Newly identified risks are added with unique IDs.

---

*End of Version 1.1 As-Built Risk Register*
