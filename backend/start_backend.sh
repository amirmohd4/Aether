#!/bin/bash
cd /app/backend
export PYTHONPATH=/app/backend
exec /root/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8001
