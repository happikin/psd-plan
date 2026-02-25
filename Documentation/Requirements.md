# CoreHub Knowledge Analytics System
## Requirements Specification (Version 1.1)

---

# 1. Introduction

This document defines the functional and non-functional requirements for the CoreHub Knowledge Analytics System MVP. The system supports ingestion, processing, analysis, and visualisation of academic and related documents in order to build a reliable internal knowledge base.

Version 1.1 introduces enhanced analytical visualisation requirements including author credibility scoring and topic evolution timeline views.

---

# 2. Functional Requirements

## 2.1 Document Ingestion

FR1.1 The system shall allow analysts to upload academic papers in PDF format.
FR1.2 The system shall extract raw textual content from uploaded PDFs.
FR1.3 The system shall support ingestion of non-academic articles in supported formats.
FR1.4 The system shall support ingestion of multiple documents in a single session.
FR1.5 The system shall validate uploaded files before processing.

---

## 2.2 Raw and Structured Data Storage

FR2.1 The system shall store extracted raw text for each uploaded document.
FR2.2 The system shall store structured, analytics-ready metadata derived from the document.
FR2.3 The system shall maintain relationships between documents, authors, keywords, and references.
FR2.4 The system shall timestamp document uploads and processing events.

---

## 2.3 Metadata and Content Extraction

FR3.1 The system shall extract document title where identifiable.
FR3.2 The system shall extract abstract where identifiable.
FR3.3 The system shall identify and extract author names where identifiable.
FR3.4 The system shall extract keywords or generate keywords through processing.
FR3.5 The system shall identify references where detectable.
FR3.6 The system shall detect publication date where available.

---

## 2.4 Analytical Processing

FR4.1 The system shall identify relationships between authors based on co-authorship.
FR4.2 The system shall identify relationships between documents based on shared keywords or similarity metrics.
FR4.3 The system shall identify relationships between authors and topics.
FR4.4 The system shall construct document reference networks.
FR4.5 The system shall support timeline-based analysis of documents.
FR4.6 The system shall perform sentiment analysis on document text.
FR4.7 The system shall support multi-dimensional linking beyond simple shared author detection.
FR4.8 The system shall compute an author credibility score derived from citation counts within the ingested dataset.
FR4.9 The system shall aggregate citation counts per author for ranking and analytical purposes.

---

## 2.5 Query and Filtering

FR5.1 The system shall provide filtering by author.
FR5.2 The system shall provide filtering by topic or keyword.
FR5.3 The system shall provide filtering by date or time range.
FR5.4 The system shall support combined query filters.
FR5.5 The system shall return query results in near-real-time for the defined dataset size.

---

## 2.6 Visualisation

FR6.1 The system shall provide graphical visualisations of relationships between documents.
FR6.2 The system shall provide graphical visualisations of author networks.
FR6.3 The system shall provide timeline visualisations.
FR6.4 The system shall provide textual or tabular views of query results.
FR6.5 The system shall provide interactive graph navigation (zoom, selection, filtering).
FR6.6 The system shall provide a graph-based view showing links between authors, topics, and documents.
FR6.7 The system shall visually represent author credibility scores within the graph view.
FR6.8 The system shall provide a timeline view showing the evolution of a selected keyword or topic across multiple years.

---

# 3. Non-Functional Requirements

## 3.1 Performance

NFR1.1 Query responses shall complete within ≤ 3 seconds for datasets up to a defined size.
NFR1.2 PDF processing time shall remain within an acceptable range per document.

## 3.2 Scalability

NFR2.1 The system shall support increasing document counts without architectural redesign.
NFR2.2 The system shall support migration to a more scalable database backend if required.

## 3.3 Maintainability

NFR3.1 The system shall follow modular architectural principles.
NFR3.2 The codebase shall follow documented coding standards.
NFR3.3 The system shall include automated testing for core components.

## 3.4 Reliability

NFR4.1 The system shall handle malformed or incomplete PDFs gracefully.
NFR4.2 The system shall prevent system crashes due to missing metadata fields.

## 3.5 Security

NFR5.1 The system shall validate uploaded files to prevent malicious input.
NFR5.2 The system shall restrict access to administrative endpoints.

## 3.6 Usability

NFR6.1 The system shall provide an accessible web-based interface.
NFR6.2 Visualisations shall be intuitive and interactive.
NFR6.3 Error messages shall be informative and actionable.

---

*End of Version 1.1 Requirements Specification*
