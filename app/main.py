# Основной файл FastAPI приложения, точка входа

from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.organizations import router as org_router
from core.config import settings
from db.session import SessionLocal, engine
from models import Base
from seed import seed_data

app = FastAPI(title="Organizations API", debug=settings.debug)


@app.on_event("startup")
def on_startup() -> None:
    """Запуск приложения. Загрузка тестовых данных"""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


app.include_router(health_router)
app.include_router(org_router)

