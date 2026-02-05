# -*- coding: utf-8 -*-
# Маршруты FastAPI (endpoints) для работы с организациями

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Organization, Activity
from schemas import OrganizationOut
from deps import get_db, api_key_auth
import methods

router = APIRouter(
    prefix="/organizations",
    dependencies=[Depends(api_key_auth)]
)

@router.get("/by-id/{org_id}", response_model=OrganizationOut)
def get_org_by_id(
        org_id: int,
        db: Session = Depends(get_db)
    ) -> OrganizationOut | None:

    return methods.organization_by_id(db, org_id)


@router.get("/in-radius/{lat}/{lon}/{radius}", response_model=list[OrganizationOut])
def get_org_in_radius(
        lat: float,
        lon: float,
        radius: float,
        db: Session = Depends(get_db)
    ) -> List[OrganizationOut]:

    return methods.organizations_in_radius(db, lat, lon, radius)


@router.get("/by-building-address/{building_address}", response_model=OrganizationOut)
def get_org_by_building_address(
        building_address: str,
        db: Session = Depends(get_db)
    ) -> OrganizationOut | None:

    return methods.organizations_by_building_address(db, building_address)


@router.get("/by-name/{org_name}", response_model=List[OrganizationOut])
def get_org_by_name(
        name: str,
        db: Session = Depends(get_db)
    ) -> List[OrganizationOut]:
    return methods.organization_by_name(db, name)


@router.get("/by-activity/{activity_name}", response_model=List[OrganizationOut])
def get_org_by_activity(
        activity_name: str,
        db: Session = Depends(get_db)
    ) -> List[OrganizationOut]:
    
    ids = methods.get_activity_tree_ids(db, activity_name)

    if not ids:
        return []

    return (
        db.query(Organization)
        .join(Organization.activities)
        .filter(Activity.id.in_(ids))
        .distinct()
        .all()
    )
