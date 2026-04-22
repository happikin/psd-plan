# Contributing to the Paper Analysis App

First off, thank you for considering contributing! This document provides detailed guidelines for contributing to this project. Our goal is to maintain a high-quality, reliable, and maintainable codebase as we move towards our MVP.

## Table of Contents
- [Contributing to the Paper Analysis App](#contributing-to-the-paper-analysis-app)
  - [Table of Contents](#table-of-contents)
  - [1. Code of Conduct](#1-code-of-conduct)
  - [2. Project Structure](#2-project-structure)
  - [3. Setting Up the Development Environment](#3-setting-up-the-development-environment)
  - [4. Coding Standards & Style](#4-coding-standards--style)
    - [4.1 Backend (Python)](#41-backend-python)
    - [4.2 Frontend (React + Tailwind)](#42-frontend-react--tailwind)
  - [5. Testing Strategy](#5-testing-strategy)
    - [5.1 Automated Testing](#51-automated-testing)
    - [5.2 UI/UX & Usability Testing](#52-uiux--usability-testing)
  - [6. Git Workflow](#6-git-workflow)
  - [7. Definition of Done (Merge Request Checklist)](#7-definition-of-done-merge-request-checklist)

---

## 1. Code of Conduct
This project and everyone participating in it is governed by the [Project Code of Conduct](../psd-assessment/Conduct.md). By participating, you are expected to uphold this code to foster an open and welcoming environment.

---

## 2. Project Structure
To satisfy the requirement for an **Organized Repository**, we strictly separate backend logic from frontend presentation. Please follow this directory structure when adding new files:

```text
paper_analysis_app/
├── src/                        # Backend Application (FastAPI)
│   ├── api/                    # API Routes/Endpoints
│   ├── core/                   # Config & Core Logic
│   ├── services/               # Business Logic (NLP, Graph Algorithms)
│   └── main.py                 # Application Entry Point
├── frontend/                   # Frontend Application (Vite + React)
│   ├── src/
│   │   ├── components/         # Reusable UI Components
│   │   │   ├── charts/         # Recharts wrappers (LineChart, PieChart)
│   │   │   ├── layout/         # Sidebar, Header, StatCards
│   │   │   └── graph/          # Knowledge Graph Visualizations
│   │   ├── hooks/              # Custom React Hooks (usePaperData, etc.)
│   │   ├── pages/              # Main Page Views (Dashboard, Ingest, Monitor)
│   │   └── App.jsx             # Main Router & Layout
│   └── tailwind.config.js      # CSS Configuration
├── tests/                      # Automated Test Suite
│   ├── unit/                   # Unit Tests (Backend)
│   └── integration/            # Integration Tests (API)
└── docs/                       # Project Documentation

```
---

## 3. Setting Up the Development Environment

### 3.1 Prerequisites
- **Python 3.9+**
- **Poetry:** [Installation Guide](https://python-poetry.org/docs/#installation)
- **Node.js 20+ & npm:** (Recommended via nvm)
- **Git**

### 3.2 Installation Steps

#### Backend Setup
1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd paper_analysis_app
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL="sqlite:///./test.db"
    ENV="development"
    ```

4.  **Run the Server:**
    ```bash
    poetry run uvicorn src.main:app --reload
    ```
    API docs available at: `http://127.0.0.1:8000/docs`

#### Frontend Setup
1.  **Navigate to frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```
    > **Note:** This installs React, TailwindCSS, Recharts, and Lucide-React.

3.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    Application available at: `http://localhost:5173`

---

## 4. Coding Standards & Style
We enforce detailed coding standards to ensure consistency across the team.

### 4.1 Backend (Python)
- **Formatter:** `Black` (line length 88).
- **Linter:** `Flake8` (to catch syntax and style errors).
- **Type Hinting:** All new functions must include Python type hints.

**Commands:**
```bash
poetry run black .
poetry run flake8 .
```

### 4.2 Frontend (React + Tailwind)
- **Functional Components:** Use functional components with Hooks (`useState`, `useMemo`). Avoid Class components.
- **Styling:** Use **Tailwind CSS** utility classes. Avoid inline `style={{...}}` unless calculating dynamic values (e.g., coordinates for the Knowledge Graph).
- **Icons:** Use `lucide-react` for all icons (e.g., `<Activity />`, `<UploadCloud />`).
- **Charts:** Isolate `Recharts` logic into separate components to keep pages clean.

**Linting Command:**
```bash
cd frontend
npm run lint
```

## 5. Testing Strategy
**Milestone Requirement:** Test implementation must be detailed and consider usability.

### 5.1 Automated Testing
- **Backend:** We use `pytest`.
    - **Unit Tests:** For data processing and NLP utilities.
    - **Integration Tests:** For API endpoints.
    ```bash
    poetry run pytest
    ```

- **Frontend:** We use `Vitest` (or Jest).
    - Ensure components render without crashing.
    ```bash
    cd frontend
    npm run test
    ```

### 5.2 UI/UX & Usability Testing (Required)
Before submitting a Merge Request involving UI changes, verify the following:

1.  **Responsiveness:**
    - Does the dashboard layout break on smaller screens (mobile/tablet)?
    - Check the `Sidebar` behavior on mobile.
2.  **Interactive Elements:**
    - **Tooltips:** Do charts show data tooltips on hover?
    - **Feedback:** Does clicking "Ingest" show a loading state (`isProcessing`) and a success notification (Toast)?
    - **Empty States:** Does the Search page handle 0 results gracefully (e.g., "No results found")?
3.  **Visual Accessibility:**
    - Ensure text contrast is sufficient (e.g., `slate-400` on `slate-900`).

---

## 6. Git Workflow
We use a **Feature Branch Workflow** to manage collaboration.

1.  **Create a Branch:**
    Never commit to `main`. Name branches descriptively:
    - `feat/add-knowledge-graph`
    - `fix/ingest-timeout`
    - `style/dashboard-colors`

2.  **Commit Messages:**
    Follow [Conventional Commits](https://www.conventionalcommits.org/):
    - `feat: Add Recharts timeline to dashboard`
    - `fix: Correct color mapping in pie chart`
    - `docs: Update contributing guide for frontend`

3.  **Push and PR:**
    Push to the remote repository and open a Merge Request.

---

## 7. Definition of Done (Merge Request Checklist)
To maintain **Organized** and **Advanced** collaboration standards, a Merge Request (MR) is considered "Done" only when:

- [ ] **Code compiles/runs** locally without errors.
- [ ] **Linting passed** (Black for Python, ESLint for JS/TS).
- [ ] **Tests passed** (All existing tests + new tests for the feature).
- [ ] **Usability Check:** Verified that UI changes are responsive and user-friendly.
- [ ] **Code Review:** At least one other team member has approved the changes.


