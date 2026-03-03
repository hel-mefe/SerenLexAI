FROM python:3.11-slim

WORKDIR /app

COPY ../backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../backend .

CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]
