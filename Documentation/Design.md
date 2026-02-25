# CoreHub Knowledge Analytics System
## Design Specification (Version 1.1)

---

# 1. High-Level System Architecture

```mermaid
flowchart TD
    User[Analyst User]
    Frontend[Web Frontend]
    Backend[FastAPI Backend]
    Ingestion[PDF Parsing Module]
    Processing[NLP & Metadata Extraction]
    Analytics[Analytics & Graph Engine]
    DB[(Structured Database)]
    RawText[(Raw Text Storage)]
    Monitoring[Logging & Monitoring]

    User --> Frontend
    Frontend --> Backend
    Backend --> Ingestion
    Ingestion --> RawText
    Ingestion --> Processing
    Processing --> DB
    Backend --> Analytics
    Analytics --> DB
    Backend --> Monitoring
    Backend --> Frontend
```

---

# 2. Data Model

```mermaid
erDiagram
    PAPER {
        int id PK
        string title
        text raw_text
        text abstract
        date publication_date
        string sentiment
        datetime uploaded_at
    }

    AUTHOR {
        int id PK
        string name
        int credibility_score
    }

    KEYWORD {
        int id PK
        string keyword
    }

    REFERENCE {
        int id PK
        string referenced_title
    }

    PAPER ||--o{ AUTHOR : written_by
    PAPER ||--o{ KEYWORD : tagged_with
    PAPER ||--o{ REFERENCE : cites
```

---

# 3. Credibility Computation

```mermaid
flowchart LR
    References --> CountCitations
    CountCitations --> UpdateCredibilityScore
    UpdateCredibilityScore --> AuthorTable
```

---

# 4. Keyword/Topic Evolution Timeline

```mermaid
flowchart TD
    UserSelect --> FilterByKeyword
    FilterByKeyword --> GroupByYear
    GroupByYear --> CountPerYear
    CountPerYear --> RenderTimeline
```

---

*End of Version 1.1 Design Specification*
