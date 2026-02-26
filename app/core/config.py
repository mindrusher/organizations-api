"""Application configuration and settings."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Centralised application settings.

    Values come from environment variables with sane defaults for local use.
    In production, override them via env vars (e.g. Docker / Kubernetes).
    """

    # Database (async driver by default)
    database_url: str = os.getenv(
        "DATABASE_URL", "mysql+aiomysql://root:root@db:3306/orgs_db"
    )

    # Security
    # Default matches README example; in production override via API_KEY env var.
    api_key: str = os.getenv("API_KEY", "API_SECRET_KEY")

    # Misc
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()

