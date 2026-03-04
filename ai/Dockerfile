FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Load tasks module so contract_intelligence.run_analysis is registered
CMD ["celery", "-A", "app.contract_intelligence.worker.tasks:celery_app", "worker", "--loglevel=info"]

