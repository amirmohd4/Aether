from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/aether_govos"
    redis_url: str = "redis://localhost:6379/0"
    active_state: str = "karnataka"
    secret_key: str = "aether-govos-secret-key-change-in-production"
    mock_failure: bool = False
    api_rate_limit: int = 100
    
    class Config:
        env_file = ".env"

settings = Settings()
