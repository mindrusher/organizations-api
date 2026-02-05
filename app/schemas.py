# -*- coding: utf-8 -*-
# Pydantic схемы для валидации данных и сериализации ответов

from pydantic import BaseModel
from typing import List

class PhoneOut(BaseModel):
    number: str

class BuildingOut(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: int | None

class OrganizationOut(BaseModel):
    id: int
    name: str
    phones: List[PhoneOut]
    building: BuildingOut
    activities: List[ActivityOut]

    class Config:
        from_attributes = True
