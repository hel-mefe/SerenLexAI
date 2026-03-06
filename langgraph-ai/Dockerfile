FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app

# Copy project metadata first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into a local .venv (no dev deps, use lockfile)
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY . .

# Default command: run Celery worker for contract_ai
# The SerenLex stack can enqueue tasks with the name "contract_ai.run_analysis"
# and payload {"analysis_id": "<uuid>", "pdf_path": "<path-or-url>"}.
CMD ["uv", "run", "celery", "-A", "contract_ai.tasks:celery_app", "worker", "--loglevel=info"]

