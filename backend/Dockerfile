FROM python:3.11-slim

# Set working directory
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cachin
COPY backend/requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy configs and scripts from parent directories
COPY ../configs /app/configs
COPY ../scripts /app/scripts

# Expose port
EXPOSE 8001

# Run database initialization and start server
CMD ["sh", "-c", "python -c 'from database import init_db; init_db()' && python /app/scripts/generate_mock_data.py && python -m uvicorn main:app --host 0.0.0.0 --port 8001"]
