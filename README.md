# SerenLexAI

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/2ffbfd32-d866-43f9-9442-19bbcb1edddd" />

SerenLexAI is a modular, AI-powered contract risk intelligence platform designed to provide structured, explainable legal analysis for non-lawyers. It is built as a composable legal inference engine rather than a chatbot wrapper: contract evaluation is decomposed into discrete stages (clause extraction, semantic classification, calibrated risk scoring, recommendation synthesis, executive summarization), each with deterministic, inspectable behavior. The system uses a multi-stage LLM pipeline, vector embeddings for clause-level semantic indexing (pgvector), asynchronous task orchestration (Celery), and graph-based workflow control (LangGraph) so that reasoning flows are auditable and configurable.

The backend is implemented with FastAPI, SQLAlchemy, and PostgreSQL, with type-safe structured outputs via Pydantic schemas to guard against malformed AI responses. Clauses are processed in parallel where appropriate, enabling scalable analysis of contracts up to a configurable page limit (default 20) while keeping token usage and context boundaries under control. The frontend is a React + TypeScript application that exposes a risk-calibrated dashboard for quick scanning and drill-down into individual clauses and recommendations. SerenLexAI supports configurable risk sensitivity, jurisdiction-aware prompting, and auditable AI decision boundaries suitable for professional use.

---

## What SerenLexAI Does

SerenLexAI ingests contracts (PDF, DOCX, or pasted text), normalizes and segments them into clause-aligned chunks, then runs a staged analysis pipeline. Each clause is classified by risk level (low, medium, high, critical), scored, and paired with a human-readable explanation and recommended action. The pipeline can optionally use prior analyses: clause embeddings are stored in PostgreSQL with the pgvector extension, and the risk classifier retrieves semantically similar clauses to inform consistency and precedent. Results are written into shared database tables (`analyses`, `clauses`, `actions`) so the same REST API that the frontend uses serves both “create analysis” and “read report” flows. Event-sourcing via the `actions` table provides a full history (e.g. upload, processing started, completed, failed) for transparency and debugging.

---

## Architecture Overview

The system is split into four main parts:

1. **Frontend** — React + TypeScript (Vite), Tailwind CSS, React Query, Zustand. Consumes the backend REST API for analyses, clauses, and history; supports document upload and text paste, with validation (e.g. PDF page limit, file size) and clear loading/error/success states.

2. **Backend API** — FastAPI application providing versioned REST endpoints (`/api/v1/...`) for analyses (list, create, upload, get by id), clauses (by analysis), and actions (history). Uses a repository/service/router layering, dependency injection via a simple registry, and Alembic for schema migrations. The API creates analysis records and enqueues Celery tasks; it does not run the LLM pipeline itself.

3. **Backend worker** — A Celery worker process that shares the backend codebase and the same broker (Redis). It is the task producer’s counterpart: the backend sends tasks with name `contract_intelligence.run_analysis`; this worker container can run other backend-defined tasks in the future. Today it primarily ensures the producer app is loadable; the actual analysis task is consumed by the AI worker.

4. **AI worker** — A separate Celery worker in the `ai/` package. It consumes `contract_intelligence.run_analysis`, runs the LangGraph pipeline (ingestion, normalization, section parsing, clause detection, risk classification with pgvector-backed precedent retrieval, scoring, recommendation, explanation, persistence), and writes results into the same PostgreSQL database the API uses. No HTTP surface; communication is via Redis (Celery) and shared DB.

Data flow in short: User submits document or text via frontend -> API validates, creates `Analysis` row, extracts text (e.g. via pdfplumber for PDF), enqueues Celery task with payload -> AI worker picks up task, runs LangGraph pipeline, updates `Analysis` and writes `Clause` and `Action` rows -> Frontend polls or refetches analyses/clauses/history from the API.

---

## Critical Technical Decisions

### Why Celery and Redis

Contract analysis is long-running and CPU/LLM-bound. Doing it inside the HTTP request would tie up workers and lead to timeouts and poor UX. Celery provides:

- **Decoupling** — The API responds immediately with “analysis created” and a status (e.g. pending/running); the client can poll or refetch. The heavy work runs in a separate process.
- **Retries and visibility** — Failed tasks can be retried with backoff; the broker (Redis) gives a single place to inspect queues and dead-letter behavior.
- **Scalability** — You can run multiple AI worker processes or multiple backend workers; the broker distributes tasks. No need to scale the API tier for CPU-heavy work.

Redis was chosen as the broker for simplicity, low operational overhead, and good support in both the backend (Python) and the AI service. The same Redis instance is used as the Celery broker and result backend so task identity and results are in one place.

### Why LangGraph

The analysis pipeline has clear stages: normalize text, parse sections, detect clauses, classify risk (with optional precedent lookup), compute scores, generate recommendations, explain, then persist. A single monolithic prompt would be hard to tune, debug, and extend. LangGraph provides:

- **Explicit DAG** — The workflow is a directed graph (normalize -> section_parser -> clause_detector -> risk_classifier -> score_calculator -> recommender -> explainer -> persister). Each node has a single responsibility; state is passed in a typed `ContractState`.
- **Inspectability** — You can log or persist state at each node, replay from a given step, and add branches (e.g. “if high risk, run extra checks”) without rewriting the whole flow.
- **Session and side effects** — Nodes that need the database (e.g. risk_classifier for pgvector retrieval, persister for writing analyses/clauses/actions) receive an async SQLAlchemy session; the graph is compiled per run with that session closed over, so persistence is consistent and testable.

Using a graph instead of one big prompt makes it easier to swap models per stage, add human-in-the-loop steps later, and keep the system maintainable as requirements evolve.

### Why pgvector

Risk classification benefits from “clauses similar to this one” from past analyses. Storing clause embeddings and querying by vector similarity is a natural fit. pgvector was chosen because:

- **Single database** — Embeddings live in PostgreSQL next to the rest of the application data. No separate vector store to operate or sync; the AI worker and the API both use the same Postgres (and the same logical schema for UI-facing tables).
- **ACID and migrations** — Schema changes and backups are handled with the same tools as the rest of the app. ivfflat (or HNSW) indexes give efficient approximate nearest-neighbor search for cosine similarity.
- **Consistency** — The AI worker writes analysis results and, where applicable, section/clause embeddings into the same DB it reads from for precedent retrieval, so there is no eventual-consistency gap between “write” and “read” stores.

The AI service uses a `contract_sections`-style table (or equivalent) with an `embedding vector(1536)` column and an index for cosine distance; the risk classifier calls an embedder and a retriever that run SQL against that table.

### Why Two Worker Containers (Backend Worker and AI Worker)

- **Backend worker** — Built from the same image as the API (backend codebase). It runs Celery with the backend’s `ai.tasks:celery_app`, which defines the producer that sends `contract_intelligence.run_analysis`. Keeping a worker in the same codebase allows you to add backend-only tasks later (e.g. cleanup, notifications, reporting) without touching the AI service. Right now it mainly ensures the producer app is valid and the queue is consumed by something if you point it at the same queue (or you can reserve it for future backend tasks).

- **AI worker** — Built from the `ai/` codebase. It runs the LangGraph pipeline, OpenAI (or other) calls, and pgvector access. Its dependencies (LangChain, LangGraph, embedding models, etc.) are heavy and different from the API’s. Isolating them in a separate image keeps the API image small and secure, and lets you scale the AI workers independently. The contract is simple: the backend sends a task payload; the AI worker consumes it and writes to the shared database. No RPC or HTTP between them.

So: two containers to separate “API + lightweight producer” from “heavy LLM + graph + vector” and to allow independent scaling and deployment of the analysis pipeline.

### Shared Database and Schema Ownership

The API and the AI worker both read and write `analyses`, `clauses`, and `actions`. The backend owns the canonical schema and migrations (Alembic) for these tables so that the REST API and the worker stay in sync. The AI service is treated as a consumer of that schema: it updates existing rows (e.g. analysis status, risk score, counts) and inserts clauses and actions. Keeping one place that defines and migrates the schema avoids drift and duplicate migration logic. The AI service may maintain its own tables (e.g. contract_sections with embeddings) in the same database; those can be migrated via the AI app’s migration scripts (e.g. SQL in `ai/app/contract_intelligence/db/migrations/`).

---

## Project Structure

```
SerenLexAI/
  backend/                 # FastAPI app, repositories, services, Celery producer
    main.py                 # App entry; mounts routers under /api/v1
    core/                   # Config, database, registry, dependencies
    api/                    # REST routers (analyses, actions)
    services/               # Business logic (analysis, clause, action)
    repositories/           # Data access (analysis, clause, action)
    models/                 # SQLAlchemy models (User, Analysis, Clause, Action)
    schemas/                # Pydantic request/response schemas
    ai/                     # Celery app and enqueue_contract_analysis
    alembic/                # Migrations for backend-owned tables
  ai/                       # Contract intelligence Celery worker
    app/contract_intelligence/
      worker/               # Celery task run_analysis, AnalysisWorker
      graph/                # LangGraph builder and runner
      nodes/                # Pipeline nodes (normalize, section_parser, ...)
      state.py              # ContractState
      tools/                # Embedder, retriever (pgvector), etc.
      db/                   # Migrations for AI-owned tables (e.g. contract_sections)
  frontend/                 # React + TypeScript (Vite)
    src/
      api/                  # Axios client, types, analysis/clause/history APIs and hooks
      pages/                # Dashboard, analyses list, new analysis, report, history
      components/           # UI (cards, filters, tables, modals, toasts)
      store/                # Zustand (filters, new analysis form state)
  infrastructure/
    docker-compose.yml      # postgres, redis, minio, api, worker, ai_worker
    api/Dockerfile          # Backend API image (migrate + uvicorn)
    worker/Dockerfile       # Backend Celery worker (ai.tasks:celery_app)
  env/                      # Environment files for Docker (postgres, backend, minio, ai)
```

---

## How to Run the Project

### Prerequisites

- Docker and Docker Compose (for full stack)
- Or, for local runs: Python 3.11+, Node 18+, PostgreSQL 16 (with pgvector), Redis, uv (Python)

### Option 1: Full stack with Docker Compose

1. **Environment files**  
   Create env files under `env/` (or adjust paths in `docker-compose.yml`):

   - `env/postgres.env`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (e.g. `serenlex`).
   - `env/backend.env`: `DATABASE_URL` (e.g. `postgresql+psycopg2://postgres:postgres@serenlex_postgres:5432/serenlex`), `REDIS_URL` (e.g. `redis://serenlex_redis:6379/0`).
   - `env/ai.env`: `DATABASE_URL` (same DB, e.g. async driver if the AI app uses asyncpg), `REDIS_URL`, `OPENAI_API_KEY` (or your LLM key).
   - `env/minio.env`: MinIO credentials if you use object storage.

2. **Build and start**  
   From the repo root:

   ```bash
   cd infrastructure
   docker compose up -d --build
   ```

   This starts Postgres (with pgvector), Redis, MinIO, the API (runs `alembic upgrade head` then `uvicorn`), the backend worker, and the AI worker. The API is on port 8000.

3. **Frontend**  
   Run the frontend locally so it can call the API:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Set `VITE_API_BASE_URL=http://localhost:8000/api/v1` in the frontend `.env` (or leave default) so the app talks to the API container.

### Option 2: Backend and AI worker locally (no Docker)

1. **PostgreSQL**  
   Create a database (e.g. `serenlex`) and enable the pgvector extension. Apply backend migrations:

   ```bash
   cd backend
   uv run alembic upgrade head
   ```

   If the AI app has its own migrations (e.g. `001_init.sql`, `002_ui_entities.sql`), run those against the same database.

2. **Redis**  
   Start Redis (e.g. `redis-server`).

3. **Backend .env**  
   In `backend/` create a `.env` with:

   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/serenlex
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Run API**  
   From repo root, with backend as the app directory:

   ```bash
   uv run uvicorn main:app --reload --app-dir backend
   ```

5. **Run backend worker** (optional):

   ```bash
   cd backend
   uv run celery -A ai.tasks:celery_app worker --loglevel=info
   ```

6. **Run AI worker**  
   From the `ai/` directory, with its own venv and `.env` (including `OPENAI_API_KEY`, `DATABASE_URL`, `REDIS_URL`):

   ```bash
   cd ai
   pip install -r requirements.txt
   celery -A app.contract_intelligence.worker.celery_app:celery_app worker --loglevel=info
   ```

7. **Frontend**  
   Same as above: `npm install`, `npm run dev`, and point `VITE_API_BASE_URL` at `http://localhost:8000/api/v1` if needed.

### Creating an analysis

- **Upload** — Use the frontend “New analysis” flow to upload a PDF (subject to page and size limits) or paste text. The API creates the analysis record and enqueues `contract_intelligence.run_analysis`. The AI worker processes it and updates status and clauses; the list and detail views show “Processing” until status is `completed` (or `failed`/`partial`).
- **API** — `POST /api/v1/analyses/upload` (multipart) or `POST /api/v1/analyses` (JSON body with title and content). List with `GET /api/v1/analyses`, detail with `GET /api/v1/analyses/{id}`, clauses with `GET /api/v1/analyses/{id}/clauses`, history with the actions endpoint.

---

## Environment Variables Summary

| Context   | Variable           | Purpose |
|----------|--------------------|--------|
| Backend  | `DATABASE_URL`     | PostgreSQL connection (sync driver, e.g. psycopg2). |
| Backend  | `REDIS_URL`        | Celery broker and result backend. |
| Backend  | `API_PREFIX`       | Optional; default `/api`. |
| Backend  | `API_VERSION`      | Optional; default `v1`. |
| Backend  | `UPLOAD_MAX_PAGES` | Max PDF pages for upload; default 20. |
| Backend  | `UPLOAD_MAX_FILE_SIZE_MB` | Max file size in MB. |
| AI       | `DATABASE_URL`     | Same PostgreSQL (async or sync as required by AI app). |
| AI       | `REDIS_URL`        | Same Redis as backend. |
| AI       | `OPENAI_API_KEY`   | For LLM and embeddings. |
| Frontend | `VITE_API_BASE_URL`| Base URL for API; e.g. `http://localhost:8000/api/v1`. |

---

## Summary

SerenLexAI is a contract risk platform that combines a FastAPI backend, a React frontend, and a dedicated AI worker. The backend exposes REST APIs and enqueues analysis tasks; the AI worker runs a LangGraph pipeline with pgvector-backed precedent retrieval and writes results into the same database. Celery and Redis provide async, scalable execution; LangGraph keeps the pipeline explicit and maintainable; pgvector keeps embeddings and relational data in one place. Two worker containers separate API-related tasks from the heavy LLM/graph/vector workload and allow independent scaling. The README image is kept as the project banner as requested.
