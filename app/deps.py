# -*- coding: utf-8 -*-
# Аутентификация по API-ключу и подключение к БД

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

API_KEY = "API_SECRET_KEY"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
