"""Конфигурации и настройки приложения."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Настройки приложения.
    Значения берутся из переменных среды для локального использования."""
    database_url: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:root@db:3306/orgs_db"
    )

    api_key: str = os.getenv("API_KEY", "API_SECRET_KEY")

    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
