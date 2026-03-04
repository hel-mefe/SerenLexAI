### Contract Intelligence Worker — Architecture

This module is a **background contract‑analysis worker**. It takes contract content from a Celery/Redis queue, runs a LangGraph pipeline with OpenAI, and writes results into the **UI entities** your backend already uses: `analyses`, `clauses`, and `actions`. There is no HTTP router here; your existing backend remains the only public surface.

---

### Core responsibilities

- **Ingestion**: Turn PDF/DOCX/text into clean, clause‑aligned `ChunkModel`s with page/position metadata.
- **Analysis workflow**: LangGraph pipeline:
  - normalize → section_parser → clause_detector → risk_classifier → score_calculator → recommender → explainer → persister
- **Persistence to UI schema**:
  - `Analysis`: overall risk, score, counts, raw_text.
  - `Clause`: per‑clause severity, explanation, recommended action.
  - `Action`: event‑sourcing stream (upload, processing started, completed, failed).

Your backend interacts with it only by:

- Enqueuing **Celery tasks**.
- Reading from **Postgres** (`analyses`, `clauses`, `actions`) the same way it reads any other CRUD tables.

---

### Data model (UI entities)

Defined in `app/contract_intelligence/models/ui_entities.py`:

- **`Analysis`** (`analyses`):
  - Links to optional `user_id`.
  - Fields: `title`, `original_filename`, `source_type` (`pdf|docx|text`), `status` (`pending|running|completed|partial|failed`), `overall_risk`, `risk_score` (0–10 → int), counts (`flagged_count`, `high_count`, `medium_count`, `low_count`), and `raw_text`.
  - Relationships: `clauses` (one‑to‑many), `actions` (event history).

- **`Clause`** (`clauses`):
  - FK: `analysis_id`.
  - Fields: `title`, `severity` (`low|medium|high|critical`), `original_text`, `risk_explanation`, `recommended_action`, optional `clause_type` and `position_index`.
  - One row per **classified clause** in the contract.

- **`Action`** (`actions`):
  - Optional FKs: `user_id`, `analysis_id`.
  - Fields: `type` (`PROCESSING_STARTED|COMPLETED|FAILED|...`), `title`, `description`, `meta` (JSONB).
  - Used for activity history / event‑sourcing in the UI.

Migration: `app/contract_intelligence/db/migrations/002_ui_entities.sql` creates these tables (expects a `users` table for `user_id`).

---

### Workflow and control flow

#### 1. Task payload (from your backend)

The Celery task uses `AnalysisTaskPayload` (`models/tasks.py`):

- `user_id: Optional[str]`
- `raw_input: str` — full contract text or base64‑encoded file
- `is_base64: bool` — `True` if `raw_input` is base64 of bytes
- `file_name: Optional[str]`
- `content_type: Optional[str]` — e.g. `application/pdf`
- `metadata: dict[str, Any]` — free‑form (`{"contract_value": 500000, "currency": "GBP"}`…)

Your backend never touches LangGraph directly; it just sends one dict matching this schema.

#### 2. Enqueueing a job

From your existing backend (Python example):

```python
from celery import Celery

app = Celery("producer", broker="redis://localhost:6379/0")

payload = {
    "user_id": "9e6e9b53-fb5a-4b71-9a8b-123456789abc",  # optional
    "raw_input": open("contract.pdf", "rb").read().decode("latin1"),  # or base64 string
    "is_base64": False,
    "file_name": "Service_Agreement.pdf",
    "content_type": "application/pdf",
    "metadata": {"contract_value": 500000, "currency": "GBP"},
}

app.send_task("contract_intelligence.run_analysis", args=[payload])
```

> If sending binary content, base64‑encode it, set `is_base64=True`, and leave `file_name`/`content_type` unchanged.

#### 3. Worker entrypoint (Celery)

- Module: `app/contract_intelligence/worker/tasks.py`
- Task name: **`contract_intelligence.run_analysis`**
- Implementation:
  - Validates the `payload` into `AnalysisTaskPayload` (Pydantic).
  - Calls `AnalysisWorker.run()` (async) inside `asyncio.run`.

#### 4. Worker service (AnalysisWorker)

Module: `app/contract_intelligence/worker/service.py`.

For each task:

1. **Decode input**:
   - If `is_base64=True`, base64‑decodes `raw_input` to bytes.
   - Otherwise uses `raw_input` as plain text.

2. **Create `Analysis` + initial `Action`**:
   - Determines `source_type` from `file_name` / `content_type` (`pdf|docx|text`).
   - Inserts an `Analysis` with:
     - `title` = `file_name` or `"Contract"`.
     - `original_filename` = `file_name`.
     - `source_type` = guessed type.
     - `status` = `"running"`.
     - `user_id` = parsed from `payload.user_id` (or null).
   - Inserts an `Action`:
     - `type` = `"PROCESSING_STARTED"`.
     - `title` = `"Document uploaded"`.
     - `description` = filename/title.
     - `meta` = `{ "filename": file_name }`.

3. **Ingestion**:
   - Calls `ingest_document(...)` with:
     - `contract_id` = `analysis.id` (used as `contract_id` inside the graph).
     - `raw_input` = string or bytes.
     - `file_name`, `content_type`.
   - `ingest_document`:
     - Detects `input_format` (`pdf|docx|text`).
     - Extracts layout‑aware blocks via `pdfplumber`/`python-docx` or text.
     - Runs the **chunker** to create clause‑aligned `chunks` with metadata.

4. **Build `ContractState`**:

- Converts `extracted_blocks` → list[`BlockModel`].
- Converts `chunks` → list[`ChunkModel`].
- Populates:
  - `contract_id` = `analysis_id`
  - `analysis_run_id` = `analysis_id` (we treat one analysis = one run)
  - `input_format`, `page_count`, `metadata` from payload
  - `analysis_id`, `user_id` so the persister can link to the UI record.

5. **Run LangGraph**:

- `run_contract_analysis(initial_state, session)`:
  - Builds the graph (`graph/builder.py`) with nodes:
    - `normalize` → `section_parser` → `clause_detector` → `risk_classifier` → `score_calculator` → `recommender` → `explainer` → `persister`
  - Invokes `app.ainvoke(initial_state)`.
  - Measures `total_latency_ms` and sets it on the returned state.

6. **Persist into UI entities (persister + ui_sync)**:

- **`persister` node**:
  - Delegates to `services/ui_sync.sync_workflow_result_to_ui(...)` using:
    - DB `session`
    - final `ContractState`
    - `analysis_id` + `user_id`.

- **`sync_workflow_result_to_ui`**:
  - **`update_analysis_from_state`**:
    - Sets `status`:
      - `"failed"` if `state.fatal_error`.
      - `"partial"` if `state.errors` non‑empty.
      - `"completed"` otherwise.
    - Sets `overall_risk` and `risk_score` (int) from deterministic scoring.
    - Counts `low|medium|high|critical` severities directly from `classified_clauses`.
    - Sets `flagged_count` = `high + critical`.
    - Aggregates `raw_text` from `extracted_blocks.text`.
  - **`upsert_clauses_for_analysis`**:
    - Deletes any existing `clauses` for this analysis.
    - For each `ClassifiedClauseModel`:
      - Computes `severity` from `risk_level`.
      - Uses `clause_type` as `title` (trimmed) or `"Clause"` fallback.
      - Writes `original_text` = `extracted_text`.
      - Writes `risk_explanation` = `risk_rationale`.
      - Computes `recommended_action` from the matching `RecommendationModel` (or falls back to rationale / default message).
      - Populates `clause_type`, `position_index`.
  - **Final `Action`**:
    - If `fatal_error` or any `errors`:
      - `type` = `"FAILED"`, with description and `meta.errors` containing error details.
    - Else:
      - `type` = `"COMPLETED"`, description summarizing risk level and score, `meta` with `risk_score` and `clause_count`.

At this point, **your backend/UI can read everything it needs from `analyses`, `clauses`, and `actions`**.

---

### How your backend consumes the results

Once a job finishes (Celery task done), your backend can:

- **List analyses** for a user:

```sql
SELECT *
FROM analyses
WHERE user_id = :user_id
ORDER BY created_at DESC;
```

- **Get a single analysis detail** (for a detail page):

```sql
SELECT *
FROM analyses
WHERE id = :analysis_id;
```

- **Get clauses for an analysis** (for the clause table / detail view):

```sql
SELECT *
FROM clauses
WHERE analysis_id = :analysis_id
ORDER BY position_index;
```

- **Get activity history** (event stream) for an analysis or user:

```sql
SELECT *
FROM actions
WHERE analysis_id = :analysis_id
ORDER BY created_at;
```

Your REST/GraphQL layer can wrap these queries into standard CRUD endpoints (e.g. `GET /analyses`, `GET /analyses/{id}`, `GET /analyses/{id}/clauses`, `GET /history`) without needing to know anything about LangGraph or LLMs.

---

### Running the worker locally

1. **Prepare environment**:
   - `.venv` with `pip install -r requirements.txt`.
   - `.env` with:
     - `OPENAI_KEY=...`
     - `DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/serenlex`
     - (optional) `REDIS_URL=redis://localhost:6379/0`

2. **Run migrations**:
   - Apply `001_init.sql` (pgvector + base tables) and `002_ui_entities.sql` (UI entities).

3. **Start infrastructure**:
   - Postgres running.
   - Redis running: `redis-server`.

4. **Start Celery worker**:

```bash
celery -A app.contract_intelligence.worker.tasks worker --loglevel=info
```

5. **Enqueue a job** from your backend or a local script as shown above.

6. **Inspect DB** to verify:
   - `analyses.status` is `"completed"` / `"failed"` / `"partial"` after processing.
   - `clauses` are populated with severities, explanations, and recommended actions.
   - `actions` contain at least `PROCESSING_STARTED` and `COMPLETED`/`FAILED`.

This is all your backend needs to know: **send a task with `AnalysisTaskPayload`, then read from the `analyses` / `clauses` / `actions` tables using your usual ORM/CRUD patterns.**

