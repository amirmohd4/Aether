FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY configs /app/configs
COPY scripts /app/scripts

EXPOSE 8001

# Only initialize database, skip mock data generation
CMD ["sh", "-c", "python -c 'from database import init_db; init_db()' && uvicorn main:app --host 0.0.0.0 --port 8001"]
