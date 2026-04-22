# Prototype Scope (MVP)

This document defines the boundaries of the Initial Prototype for Milestone 1. It clarifies the "Vertical Slice" of functionality implemented to demonstrate value, while distinguishing between **Implemented Interface** and **Designed Architecture**.

## 1. In-Scope: Frontend Implementation (High-Fidelity)
The user-facing layer is fully implemented to validate the "Visual Analytics" value proposition with the client.

* **User Interface (UI) Shell:** Complete React-based Single Page Application (SPA) with Sidebar navigation and responsive layout.
* **Interactive Visualization:**
    * Force-directed Knowledge Graph with SVG rendering (Nodes: Authors, Papers, Topics).
    * Temporal Playback control for time-series filtering (Client Requirement: Topic Evolution).
* **Dashboard Analytics:** Real-time calculation of statistics (Total Papers, Topic Distribution) based on the active dataset.
* **Reporting:** "Briefing Mode" modal for automated report generation.

## 2. In-Scope: Backend Architecture & Ingestion Design
While the frontend currently uses mock data for stability, the backend architecture has been defined and partially scripted to prepare for integration.

* **Data Ingestion Logic (Designed):**
    * **PDF Parsing:** Logic defined for validating file formats and stripping non-text elements.
    * **Keyword Extraction:** Selection of the **RAKE (Rapid Automatic Keyword Extraction)** engine (Python) to parse abstracts, replacing heavier NLP libraries like Spacy.
    * **Compliance:** "Ingest-and-Discard" workflow designed to ensure no PDF files are permanently stored, strictly adhering to copyright constraints.
* **Data Model (Defined):**
    * **Database Choice:** **MongoDB** selected for its hierarchical document structure (Document -> Title -> Author -> References).
    * **Metadata Schema:** JSON schema defined to store Title, Author, References, and extracted Keywords.

## 3. Out-of-Scope (Deferred to Future Milestones)
To manage development risk and resource constraints, the *integration* of these layers is deferred:

* **Live Full-Stack Integration:**
    * The prototype currently uses local state (`INITIAL_DATA`) to simulate the database.
    * *Reasoning:* Connecting the React frontend to the live MongoDB instance is scheduled for Milestone 2. This allows the Frontend and Backend streams to be developed in parallel without blocking each other.
* **Advanced LaTeX Parsing:**
    * While the requirement to support LaTeX equations is identified[cite: 8], the parsing logic is currently simplified to text-only for the Milestone 1 demo.
* **User Authentication:** Multi-user login is not implemented; the system assumes a single active session.

## 4. Rationale for Scope Definition
The scope prioritizes **Risk Reduction** through a decoupled strategy:

1.  **Value Risk (Frontend Focus):** By building the *Visualization* features first, we validate that the tool solves the "Information Overload" problem before investing in complex backend wiring.
2.  [cite_start]**Feasibility Risk (Backend Focus):** By defining the MongoDB schema  [cite_start]and RAKE logic  [cite_start]early (without waiting for the UI), we ensure the data strategy is feasible and GDPR-compliant[cite: 12].
3.  **Usability Risk:** Using mock data allows for stable user testing of complex interactions (e.g., Timeline Slider) without server latency issues.