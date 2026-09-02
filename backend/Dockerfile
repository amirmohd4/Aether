FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend/
COPY configs /app/configs
COPY scripts /app/scripts

EXPOSE 8081

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8081"]
