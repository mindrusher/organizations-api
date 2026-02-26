"""SQLAlchemy async engine and session management."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# echo SQL only in debug mode to avoid noisy logs in production
engine = create_async_engine(settings.database_url, echo=settings.debug)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

