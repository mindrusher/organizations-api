# -*- coding: utf-8 -*-
# SQLAlchemy, модели таблиц базы данных

from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base

class Building(Base):
    """
    Модель здания.
    
    Хранит информацию о местоположении.
    Одно здание может содержать несколько организаций.

    Attributes:
        id: int - Уникальный идентификатор здания
        address: str - Адресс здания
        latitude: float - Широта, где расположено здание
        longitude: float - Долгота, где расположено здание
        
        organizations: Связь с организацией которая находится в здании
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    """
    Модель вида деятельности с иерархической структурой.
    
    Attributes:
        id: int - Уникальный идентификатор
        name: str - Название деятельности
        parent_id: int - Идентификатор родительской деятельности
        
        parent: Связь с родительской деятельностью организации
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey("activities.id"))

    parent = relationship("Activity", remote_side=[id], backref="children")


class Organization(Base):
    """
    Модель организации.

    Attributes:
        id: int - Уникальный идентификатор
        name: str - Название организации
    
    Основная бизнес-сущность системы. Связана с:
    - Зданием (где расположена)
    - Видами деятельности (чем занимается)
    - Телефонами (контактная информация)
    """
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity",
        secondary="organization_activities",
        backref="organizations"
    )

    phones = relationship("Phone", cascade="all, delete-orphan")


class Phone(Base):
    """Модель телефонного номера организации.
    
    Хранит телефонный номер, номеров может быть несколько у одной организации.

    Attributes:
        id: int - Уникальный идентификатор
        number: str - Номер
        
        organization_id: Связь с организацией к которой прикреплен номер
    """
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    number = Column(String(32), unique=True, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))


class OrganizationActivity(Base):
    """
    Таблица связи многие ко многим между организациями и видами деятельности.
    
    Вспомогательная таблица для связи Organization и Activity.
    """
    __tablename__ = "organization_activities"

    organization_id = Column(
        Integer, ForeignKey("organizations.id"), primary_key=True
    )
    activity_id = Column(
        Integer, ForeignKey("activities.id"), primary_key=True
    )
