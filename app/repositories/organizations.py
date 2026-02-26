"""Repository layer for organization-related data access (async)."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Activity, Building, Organization


class OrganizationRepository:
    """Repository for ``Organization`` and related entities.

    Hides raw ORM queries behind a small, testable API.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, org_id: int) -> Optional[Organization]:
        return await self._db.get(Organization, org_id)

    async def get_by_name(self, name: str) -> List[Organization]:
        result = await self._db.scalars(
            select(Organization).where(Organization.name.ilike(f"%{name}%"))
        )
        return result.all()

    async def get_by_building_address(
        self, building_address: str
    ) -> Optional[Organization]:
        result = await self._db.scalars(
            select(Organization)
            .join(Building)
            .where(Building.address == building_address)
        )
        return result.first()

    async def get_in_radius(
        self, lat: float, lon: float, radius: float
    ) -> List[Organization]:
        """Return organizations within a simple radius around a point."""
        buildings_subq = (
            select(Building.id)
            .where(
                func.pow(Building.latitude - lat, 2)
                + func.pow(Building.longitude - lon, 2)
                <= func.pow(radius, 2)
            )
        )

        result = await self._db.scalars(
            select(Organization).join(Building).where(Building.id.in_(buildings_subq))
        )
        return result.all()

    async def get_activity_tree_ids(self, activity_name: str) -> list[int]:
        """Return activity IDs for the given node and all its descendants."""
        root = await self._db.scalar(
            select(Activity).where(Activity.name == activity_name)
        )
        if not root:
            return []

        result: list[int] = [root.id]
        queue: list[int] = [root.id]

        while queue:
            current = queue.pop(0)
            children_result = await self._db.scalars(
                select(Activity).where(Activity.parent_id == current)
            )
            children = children_result.all()
            for child in children:
                result.append(child.id)
                queue.append(child.id)

        return result

    async def get_by_activity_ids(self, activity_ids: list[int]) -> List[Organization]:
        """Return all organizations matching any of the given activity IDs."""
        if not activity_ids:
            return []

        stmt = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .distinct()
        )
        result = await self._db.scalars(stmt)
        return result.all()
