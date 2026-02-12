"""FastAPI зависимости (DB sessions, auth, services)."""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from db.session import SessionLocal
from repositories.organizations import OrganizationRepository
from services.organizations import OrganizationService


def get_db() -> Session:
    """Предоставляет сеанс бд для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def api_key_auth(x_api_key: str = Header(...)) -> None:
    """API-key аутентификация.

    The key is provided via ``X-API-Key`` header and compared
    against the configured value.
    """
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


def get_organization_service(db: Session = Depends(get_db)) -> OrganizationService:
    """Фабричный подход для OrganizationService с шаблоном репозитория."""
    repo = OrganizationRepository(db)
    return OrganizationService(repo)



