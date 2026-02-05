# -*- coding: utf-8 -*-
# Основной файл FastAPI приложения, точка входа

from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base
from routers import router as org_router
from seed import seed_data

app = FastAPI(title="Organizations API")

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    """Загружаем тестовые данные при сборке контейнера"""
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

app.include_router(org_router)
