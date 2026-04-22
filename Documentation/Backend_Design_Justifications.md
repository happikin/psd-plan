# Backend Design Justification

## 1\. Purpose of this Document

This Document focuses on the justifications for each decision made with regards to the prototype design and future full software design.

Initial design decisions: 1. title extraction from uploaded PDFs 2. storing extracted raw text from each paper for future ML analysis

The reasons behind these choices were for balancing delivery speed, technical simplicity, storage constraints, and future compatibility with LLM-driven workflows for a full product.

# 2\. Justification: Title Extraction

## Decision

The system extracts the paper title immediately during PDF ingestion, using the following fallback order:

- PDF metadata title
- first meaningful line of extracted text
- filename stem

## Justification

The prototype had limited development time, so it was important to identify the **minimum information required to make uploaded papers searchable for a frontend system**. The title provides good usability whilst being simple to extract.

### Benefits

### 2.1 Fast Prototype Delivery

Title extraction can be implemented with very little processing overhead compared with more advanced metadata extraction such as:

- author parsing
- reference linking

This allowed the prototype to demonstrate value while avoiding delayed complex metadata extraction and NLP for keyword extraction for example.

### 2.2 Document Identification

A title provides a strong relatable identifier for:

- UI
- database browsing
- debugging
- manual correctness testing

Without a title, uploaded papers would use unique unrelated IDs.

### 2.3 Supports Incremental Metadata Enrichment

Extracting the title first, the system makes use of a robust document identity that future components rely upon:

- authors
- abstract
- references
- citation credibility
- keyword topics

# 3\. Justification: Raw Text Extraction

## Decision

The prototype stores:

- extracted raw_text
- extracted title

and deliberately avoids storing the original PDF binary.

## Why this was chosen

A key constraint in the prototype environment was that **PDF files themselves could not be persistently stored**, whether due to legal/data constraints.

raw-text extraction was therefore the most practical and obvious decision for representating each paper.

## 3.1 Data Model

The data model is made simpler and easier as raw text allows the database schema to remain lightweight:

Paper(id, title, raw_text)

rather than requiring file object storage for example

## 3.2 LLM Benefits

The most important technical justification is that raw text is consumable by large language models (LLMs).

The roadmap for this prototype includes:

- keyword extraction
- citation analysis
- credibility scoring

Extracting raw text at ingestion time, the system avoids repeated PDF parsing every time an LLM task is executed.

This creates a much cleaner downstream pipeline:

PDF -> raw_text -> LLM tasks

rather than repeatedly doing:

PDF -> parse -> clean -> LLM

for every request.

This decision reduces complexity and compute duplication.

## 3.3 Keyword Extraction

A future feature is automated keyword extraction.

Raw text is ideal for by enabling:

- section-aware parsing
- embedding generation
- LLM keyword extraction

This makes the prototype significantly easier to extend into:

- researching papers related to a topic a user wants to understand.
- search systems

## 3.4 Iterative design process benefits

For the iterative design process repeated operations such as:

- credibility recomputation
- reference extraction
- citation counts

become much faster when raw text is already persisted.