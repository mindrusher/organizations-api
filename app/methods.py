"""Т.к. пересобрал решение тз под прод-версию, фасад устаревший, бизнес логика в services
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from models import Organization
from repositories.organizations import OrganizationRepository
from services.organizations import OrganizationService


def _make_service(db: Session) -> OrganizationService:
    repo = OrganizationRepository(db)
    return OrganizationService(repo)


def organizations_by_building_address(
    db: Session, building_address: str
) -> Optional[Organization]:
    return _make_service(db).get_by_building_address(building_address)


def organization_by_id(db: Session, org_id: int) -> Optional[Organization]:
    return _make_service(db).get_by_id(org_id)


def organization_by_name(db: Session, name: str) -> List[Organization]:
    return _make_service(db).get_by_name(name)


def organizations_in_radius(
    db: Session, lat: float, lon: float, radius: float
) -> List[Organization]:
    return _make_service(db).get_in_radius(lat, lon, radius)


def get_activity_tree_ids(db: Session, activity_name: str) -> list[int]:
    repo = OrganizationRepository(db)
    return repo.get_activity_tree_ids(activity_name)

