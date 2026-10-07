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

# worker.py starts the web API plus the durable worker when
# AETHER_EMBED_WORKER=true; otherwise it runs worker-only.
CMD ["python", "backend/worker.py"]
