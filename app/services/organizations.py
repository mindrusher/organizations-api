"""Слой обработки Организации"""

from typing import List, Optional

from models import Organization
from repositories.organizations import OrganizationRepository


class OrganizationService:
    """Класс инкапсулирующий методы использования, связанные с организацией."""

    def __init__(self, repo: OrganizationRepository) -> None:
        self._repo = repo

    def get_by_id(self, org_id: int) -> Optional[Organization]:
        return self._repo.get_by_id(org_id)

    def get_by_name(self, name: str) -> List[Organization]:
        return self._repo.get_by_name(name)

    def get_by_building_address(self, building_address: str) -> Optional[Organization]:
        return self._repo.get_by_building_address(building_address)

    def get_in_radius(self, lat: float, lon: float, radius: float) -> List[Organization]:
        return self._repo.get_in_radius(lat, lon, radius)

    def get_by_activity(self, activity_name: str) -> List[Organization]:
        ids = self._repo.get_activity_tree_ids(activity_name)
        if not ids:
            return []
        return self._repo.get_by_activity_ids(ids)

