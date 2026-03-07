FROM ghcr.io/astral-sh/uv:python3.11-bookworm

WORKDIR /app

# pdf2image needs poppler-utils; pytesseract needs tesseract-ocr for OCR
RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy everything needed for uv sync (metadata + source so setuptools can find the package)
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies into a local .venv (frozen from lockfile, no dev deps)
RUN uv sync --frozen --no-dev

# Copy the rest of the application code (tests, configs, etc.)
COPY . .

# Default command: run Celery worker for contract_ai
# The SerenLex stack enqueues tasks with the name "contract_ai.run_analysis"
# and payload {"analysis_id": "<uuid>", "pdf_path": "<path-or-url>"}.
CMD ["uv", "run", "python", "-m", "celery", "-A", "contract_ai.tasks:celery_app", "worker", "--loglevel=info"]
