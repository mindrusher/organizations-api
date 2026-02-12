"""Healthcheck endpoints for monitoring and orchestration."""

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from db.session import SessionLocal


router = APIRouter(tags=["health"])


@router.get("/health", summary="Basic healthcheck")
def healthcheck() -> dict:
    """Lightweight healthcheck endpoint.

    - Verifies that the application is up.
    - Performs a minimal database check.
    """
    db_status = "unknown"
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db_status = "up"
        finally:
            db.close()
    except SQLAlchemyError:
        db_status = "down"

    status = "ok" if db_status == "up" else "degraded"

    return {
        "status": status,
        "checks": {
            "database": db_status,
        },
    }

