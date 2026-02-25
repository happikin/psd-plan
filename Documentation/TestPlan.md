# CoreHub Knowledge Analytics System
## Test Plan (Version 1.0 Baseline)

---

# 1. Testing Objectives

- Validate PDF ingestion and metadata extraction.
- Verify relational data integrity.
- Ensure author credibility computations are accurate.
- Confirm timeline aggregation correctness.
- Validate query logic and graph data generation.

---

# 2. Testing Levels

## Unit Testing
- PDF text extraction
- Metadata extraction
- Keyword extraction
- Reference extraction
- Credibility computation
- Query filtering logic

## Integration Testing
- Upload → Store → Process → Compute Credibility
- Keyword selection → Timeline generation

## System Testing
- Full ingestion-to-visualisation workflow
- Graph integrity validation
- Timeline correctness validation

## Performance Testing
- Query response time ≤ 3 seconds
- Processing time per document

---

# 3. Continuous Integration

- All merge requests trigger automated tests.
- Coverage reports generated automatically.
- Build fails if tests do not pass.

---

*End of Version 1.0 Test Plan*
