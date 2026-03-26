#!/usr/bin/env python3
"""
Startup script for Aether GovOS Backend
"""
import sys
import os

# Set Python path
sys.path.insert(0, '/app/backend')
os.chdir('/app/backend')

# Import and run
if __name__ == "__main__":
    import uvicorn
    from main import app
    
    print("🚀 Starting Aether GovOS Backend...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
