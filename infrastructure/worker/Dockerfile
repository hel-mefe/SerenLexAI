FROM python:3.11-slim

WORKDIR /app

# System dependencies required for psycopg2 and Postgres client libraries
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv to resolve dependencies from pyproject.toml / uv.lock
RUN pip install --no-cache-dir uv

# Copy project metadata and install dependencies into the system environment
COPY pyproject.toml uv.lock ./
RUN uv pip install --system .

# Copy backend source code
COPY . .

# NOTE: adjust the Celery app path when you add a concrete celery_app module
CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]
