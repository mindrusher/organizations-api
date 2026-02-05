# -*- coding: utf-8 -*-
# Загрузка тестовых данных при сборке контейнера

from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Building, Activity, Organization, Phone


def seed_data(db: Session):
    # --------- Здания ---------
    if db.scalar(select(Building).limit(1)):
        return

    building_1 = Building(
        address="Москва, ул. Блюхера, д. 16",
        latitude=55.5833,
        longitude=38.1788,
    )

    building_2 = Building(
        address="Москва, ул. Блюхера, д. 2",
        latitude=55.5852,
        longitude=38.1738,
    )

    building_3 = Building(
        address="Москва, ул. Карла Маркса, д. 38",
        latitude=55.589,
        longitude=38.1656,
    )

    building_4 = Building(
        address="Москва, ул. Авиационная, д. 32",
        latitude=55.5913,
        longitude=38.1835,
    )

    db.add_all([building_1, building_2, building_3, building_4])
    db.flush()

    # --------- Деятельность организаций ---------
    food = Activity(name="Еда")
    meat = Activity(name="Мясная продукция", parent=food)
    milk = Activity(name="Молочная продукция", parent=food)

    cars = Activity(name="Автомобили")
    light = Activity(name="Легковые", parent=cars)
    cargo = Activity(name="Грузовые", parent=cars)

    light_parts = Activity(name="Запчасти", parent=light)
    light_acc = Activity(name="Аксессуары", parent=light)

    cargo_parts = Activity(name="Запчасти (грузовые)", parent=cargo)
    cargo_acc = Activity(name="Аксессуары (грузовые)", parent=cargo)

    db.add_all([
        food, meat, milk,
        cars, light, cargo,
        light_parts, light_acc,
        cargo_parts, cargo_acc
    ])
    db.flush()

    # --------- Организации ---------
    org_1 = Organization(
        name='ООО "Рога"',
        building=building_1,
        activities=[food, meat],
        phones=[Phone(number="+79990000001")]
    )

    org_2 = Organization(
        name='ООО "Хвост"',
        building=building_2,
        activities=[food, meat, milk],
        phones=[Phone(number="+79990000002")]
    )

    org_3 = Organization(
        name='ОАО "Копыта"',
        building=building_3,
        activities=[cars, light, light_parts, light_acc],
        phones=[Phone(number="+79990000003"), Phone(number="+79990000004")]
    )

    org_4 = Organization(
        name='ИП "Ухов Глаз Шкурович"',
        building=building_4,
        activities=[cars, light, cargo, light_parts, cargo_parts, cargo_acc],
        phones=[Phone(number="+79990000005"), Phone(number="+79990000006")]
    )

    db.add_all([org_1, org_2, org_3, org_4])
    db.commit()
