"""Слой для доступа к данным, связанным с организацией"""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import Activity, Building, Organization


class OrganizationRepository:
    """Репозиторий для Организации и связанных с ней объектов"""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, org_id: int) -> Optional[Organization]:
        return self._db.get(Organization, org_id)

    def get_by_name(self, name: str) -> List[Organization]:
        return self._db.scalars(
            select(Organization).where(Organization.name.ilike(f"%{name}%"))
        ).all()

    def get_by_building_address(self, building_address: str) -> Optional[Organization]:
        return self._db.scalars(
            select(Organization)
            .join(Building)
            .where(Building.address == building_address)
        ).first()

    def get_in_radius(self, lat: float, lon: float, radius: float) -> List[Organization]:
        buildings_subq = (
            select(Building.id)
            .where(
                func.pow(Building.latitude - lat, 2)
                + func.pow(Building.longitude - lon, 2)
                <= func.pow(radius, 2)
            )
        )

        return self._db.scalars(
            select(Organization).join(Building).where(Building.id.in_(buildings_subq))
        ).all()

    def get_activity_tree_ids(self, activity_name: str) -> list[int]:
        root = self._db.scalar(select(Activity).where(Activity.name == activity_name))
        if not root:
            return []

        result: list[int] = [root.id]
        queue: list[int] = [root.id]

        while queue:
            current = queue.pop(0)
            children = self._db.scalars(
                select(Activity).where(Activity.parent_id == current)
            ).all()
            for child in children:
                result.append(child.id)
                queue.append(child.id)

        return result

    def get_by_activity_ids(self, activity_ids: list[int]) -> List[Organization]:
        if not activity_ids:
            return []

        return (
            self._db.query(Organization)
            .join(Organization.activities)
            .filter(Activity.id.in_(activity_ids))
            .distinct()
            .all()
        )

