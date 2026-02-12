"""API поинты для организаций"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas import OrganizationOut
from api.deps import api_key_auth, get_organization_service
from services.organizations import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/by-id/{org_id}", response_model=OrganizationOut)
def get_org_by_id(
    org_id: int,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationOut:
    """Возвращает организацию по её ID"""
    org = service.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/in-radius/{lat}/{lon}/{radius}", response_model=list[OrganizationOut])
def get_org_in_radius(
    lat: float,
    lon: float,
    radius: float,
    service: OrganizationService = Depends(get_organization_service),
) -> List[OrganizationOut]:
    """Возвращает список организаций в радиусе от точки, где:
    lat и lon - широта и долгота центра окружности,
    radius - соответственно радиус окружности с центром в точке
    указанной выше.
    Функция не использует точное геопозиционирование, за основу
    взята формула определния принадлежности точки к окружности
    """
    return service.get_in_radius(lat, lon, radius)


@router.get("/by-building-address/{building_address}", response_model=OrganizationOut)
def get_org_by_building_address(
    building_address: str,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationOut:
    """Возвращает организацию по адресу здания"""
    org = service.get_by_building_address(building_address)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/by-name/{org_name}", response_model=List[OrganizationOut])
def get_org_by_name(
    org_name: str,
    service: OrganizationService = Depends(get_organization_service),
) -> List[OrganizationOut]:
    """Возвращает список организаций по имени (также частичное совпадение)"""
    return service.get_by_name(org_name)


@router.get("/by-activity/{activity_name}", response_model=List[OrganizationOut])
def get_org_by_activity(
    activity_name: str,
    service: OrganizationService = Depends(get_organization_service),
) -> List[OrganizationOut]:
    """Возвращает список организаций по роду деятельности (имени|Activities.name)"""
    return service.get_by_activity(activity_name)


