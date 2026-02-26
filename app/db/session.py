"""SQLAlchemy engine and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# echo SQL only in debug mode to avoid noisy logs in production
engine = create_engine(settings.database_url, echo=settings.debug)

# In a bigger app you may want scoped_session here
SessionLocal = sessionmaker(bind=engine)

