# CoreHub Knowledge Analytics System
## Risk Register (Version 1.0 Baseline)

---

# 1. Risk Management Methodology

Risks are assessed using a quantitative scoring model:

- Probability (P): Rated 1–5
- Impact (I): Rated 1–5
- Risk Score = P × I

Risk Levels:
- Low: 1–6
- Medium: 7–14
- High: 15–25

Risks are reviewed at the end of each sprint and updated accordingly.

---

# 2. Risk Register Table

| ID | Risk Description | Category | P | I | Score | Level | Mitigation Strategy | Owner | Status |
|----|------------------|----------|---|---|-------|-------|---------------------|--------|--------|
| R1 | PDF parsing inconsistencies due to layout variability | Technical | 3 | 4 | 12 | Medium | Use heuristic-based extraction and test against sample dataset | Backend Lead | Mitigated (Monitoring) |
| R2 | Scope creep due to large number of analytical features | Project | 4 | 3 | 12 | Medium | Use priority-based requirement classification and freeze P1 scope | Project Lead | Open |
| R3 | NLP complexity exceeding team expertise | Technical | 2 | 3 | 6 | Low | Use deterministic NLP methods instead of advanced ML | Data Lead | Mitigated (Monitoring) |
| R4 | Uneven workload distribution across 5-member team | Organisational | 3 | 4 | 12 | Medium | Assign clear role ownership and conduct weekly check-ins | Project Lead | Open |
| R5 | Performance degradation with increasing dataset size | Technical | 3 | 4 | 12 | Medium | Implement indexing and monitor query execution times early | Backend Lead | Open |
| R6 | Failure to meet deployment requirements | Operational | 2 | 4 | 8 | Medium | Create Docker prototype early in development cycle | DevOps Lead | Open |
| R7 | Insufficient automated testing coverage | Quality | 3 | 4 | 12 | Medium | Define minimum coverage target (>=60%) and enforce CI checks | QA Lead | Open |
| R8 | Loss of data integrity during processing pipeline updates | Technical | 2 | 4 | 8 | Medium | Store raw text and version processing logic | Backend Lead | Mitigated (Monitoring) |
| R9 | Delays due to milestone feedback requiring redesign | Project | 3 | 3 | 9 | Medium | Freeze baseline design early and document decisions clearly | Project Lead | Open |

---

# 3. Risk Review Process

- Risks are reviewed at sprint review meetings.
- Scores may be updated based on new information.
- Closed risks are retained in the register with updated status for traceability.
- Newly identified risks are added with unique IDs.

---

*End of Version 1.0 Baseline Risk Register*
