from pathlib import Path

from pydantic_settings import BaseSettings
from functools import lru_cache

# Project root: Hindsight/
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    app_name: str = "Regret Pill API"
    app_version: str = "0.1.0"
    debug: bool = True

    # DashScope
    dashscope_api_key: str = ""
    dashscope_model: str = "qwen-plus"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # PostgreSQL
    database_url: str = "postgresql+asyncpg://regret:regret_dev_2024@localhost:5432/regret_pill"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Simulation
    simulation_timeout: int = 120  # seconds
    max_simulation_steps: int = 10

    model_config = {
        "env_file": str(_ENV_FILE),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
