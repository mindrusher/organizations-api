"""SQLAlchemy и обработка сессий."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для ORM моделей."""
    pass


engine = create_engine(settings.database_url, echo=settings.debug)

SessionLocal = sessionmaker(bind=engine)
