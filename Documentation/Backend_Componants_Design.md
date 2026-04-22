# MVP Backend Components Design

## 1\. System Overview

The backend built with FastAPI primarily accepts uploaded PDF files, extract text content, persist the extracted document with associated metadata e.g Title into a relational database, returning document identifiers.

### Request Flow

- Client sends POST
- API creates DB session.
- PDF parser extracts title + raw text from papwe.
- Storage service stores result of PDF parser
- API returns {status, paper_id}.

# 2\. Component: API Layer (main.py)

## Responsibility

- Expose HTTP endpoints
- Validate incoming file uploads
- Coordinate service calls
- Convert internal exceptions into HTTP responses

## Public Interface

### Endpoint

POST /upload

### Input

- file: UploadFile
- MIME type: application/pdf

### Output

{  
"status": "success",  
"paper_id": 1  
}

## Internal Logic

### Method: upload_pdf(file, db)

**Steps** 1. Validate file exists 2. Acquire DB session 3. Call extract_text_from_pdf(file) 4. Call store_raw_text(db, raw_text, title) 5. Return response payload 6. Close DB session

## Failure Modes

- Empty PDF → 422
- Parser failure → 500
- DB insert failure → 500

# 3\. Component: PDF Parser Service (services/pdf_parser.py)

## Responsibility

Convert PDF into useable text and title

## Public Interface

extract_text_from_pdf(file: UploadFile) -> dict

## Output Contract

{  
"title": str,  
"raw_text": str  
}

## Internal Processing Steps

### Step 1: Validation

- Ensure binary payload is non-empty

### Step 2: Reader Construction

- Read file bytes using BytesIO module
- Initialise PdfReader

### Step 3: Paper Page Iteration

For each page:

- call page.extract_text() extracting plain text from pdf associating this with python list.
- append non-empty text

### Step 4: Title Resolution

Priority order: 1. PDF metadata /Title 2. first non-empty extracted line 3. uploaded filename stem

# 4\. Component: Storage Service (services/storage_service.py)

## Responsibility

Store raw text and title parsed from PDF into database.

## Public Interface

store_raw_text(db: Session, raw_text: str, title: str) -> int

## Internal Steps

- Validate raw_text not empty
- Construct Paper ORM entity
- db.add(entity)
- db.commit()
- db.refresh(entity)
- return entity.id

## Error case

- schema mismatch
- text exceeds DB limits

# 5\. Component: Database Session Layer (database.py)

## Responsibility

Provide SQLAlchemy engine and managed sessions.

## Public Interfaces

engine  
SessionLocal  
get_db()

## Design

### Engine

create_engine(DB_URL)

### Session Factory

sessionmaker(bind=engine)

### Dependency Provider

def get_db():  
db = SessionLocal()  
try:  
yield db  
finally:  
db.close()

## Notes

- connection pooling enabled by SQLAlchemy
- one session per request

# 6\. Component: ORM Data Model (models.py)

## Responsibility

Represent persisted paper metadata and extracted text.

## Entity: Paper

### Fields

- id: Integer (PK)
- title: String
- raw_text: Text
- created*at: DateTime *(recommended)\_

## Example Schema

class Paper(Base):  
\_\_tablename\_\_= "papers"  
<br/>id = Column(Integer, primary_key=True)  
title = Column(String(500), nullable=False)  
raw_text = Column(Text, nullable=False)

## Indexing Recommendation

- PK index on id
- optional full-text index on raw_text

# 7\. Future Backend Components

## Extend MVP design for Document Search Service

- search by title
- keyword search over raw_text

# Credibility Computation for Paper PDFs

## 1\. Responsibilities

This component is responsible for:

- extracting the references section from parsed PDF text
- identifying individual citation entries
- counting total citations
- computing a credibility score based on defined algorithm based on citations

## 2\. Subcomponents

## 2.1 Reference Extraction Service

### Module

services/reference_extractor.py

### Responsibility

Locate and isolate the references/bibliography section from raw_text.

### Interface

extract_references(raw_text: str) -> list\[str\]

### Internal Logic

- Search for section headers:
  - Bibliography
- Split text from that point onward
- Split and assign individual reference strings

## 3.2 Citation Counting Service

### Module

services/citation_counter.py

### Responsibility

Count extracted references performing a citation ratio between 0 and 1 between total citations.

### Interface

count_citations(references: list\[str\]) -> dict

### Output Contract

{

"citation_count": 42,

"valid_citation_ratio": 0.91

}

### Internal Rules

- total count = number of parsed references
- calculate percentage of valid-looking entries

### Validation Heuristics

A citation is considered valid if it contains:

- author present in the DB
- associated year present in the DB
- associated title present in the DB

## 3.3 Credibility Score Engine

### Module

services/credibility_engine.py

### Responsibility

Convert citation-derived features into a scalar credibility score.

### Interface

compute_credibility_score(citation_count: int, valid_ratio: float) -> float

### Scoring Formula

Recommended baseline:

credibility_score =

- 60% citation volume contribution
- 40% citation quality contribution

Inline formula:

score = min(citation_count / 100, 1.0) \* 0.6 + valid_ratio \* 0.4

### Score Range

- 0.0 = weak credibility
- 1.0 = strong credibility

### Example

citation_count = 80

valid_ratio = 0.9

score = 0.84