# -*- coding: utf-8 -*-
# Бизнес-логика и запросы к базе данных

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import Organization, Building, Activity


def organizations_by_building_address(db: Session, building_address: str) -> Optional[Organization]:
    """Возвращает организацию по адресу здания или None"""
    return db.scalars(
        select(Organization).join(Building).where(Building.address == building_address)
    ).first()


def organization_by_id(db: Session, org_id: int) -> Optional[Organization]:
    """Возвращает организацию по её ID или None"""
    return db.get(Organization, org_id)


def organization_by_name(db: Session, name: str) -> List[Organization]:
    """Возвращает список организаций по имени (также частичное совпадение)"""
    return db.scalars(
        select(Organization).where(Organization.name.ilike(f"%{name}%"))
    ).all()


def organizations_in_radius(
        db: Session, lat: float, lon: float, radius: float
    ) -> List[Organization]:
    """Возвращает список организаций в радиусе от точки, где:
    lat и lon - широта и долгота центра окружности,
    radius - соответственно радиус окружности с центром в точке
    указанной выше.
    Функция не использует точное геопозиционирование, за основу
    взята формула определния принадлежности точки к окружности
    """
    
    buildings_subq = (
        select(Building.id)
        .where(
            func.pow(Building.latitude - lat, 2) +
            func.pow(Building.longitude - lon, 2)
            <= func.pow(radius, 2)
        )
    )

    return db.scalars(
        select(Organization)
        .join(Building)
        .where(Building.id.in_(buildings_subq))
    ).all()


def get_activity_tree_ids(db: Session, activity_name: str) -> list[int]:
    """Возвращает список организаций по роду деятельности (имени|Activities.name)"""
    root = db.scalar(
        select(Activity).where(Activity.name == activity_name)
    )

    if not root:
        return []

    result = [root.id]
    queue = [root.id]

    while queue:
        current = queue.pop(0)

        children = db.scalars(
            select(Activity).where(Activity.parent_id == current)
        ).all()

        for child in children:
            result.append(child.id)
            queue.append(child.id)

    return result
