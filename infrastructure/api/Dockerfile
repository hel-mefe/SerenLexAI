FROM python:3.11-slim

WORKDIR /app

COPY ../backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../backend .

COPY ../infrastructure/scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
