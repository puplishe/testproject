import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    submenus = relationship(
        'Submenu', back_populates='menus', cascade='all,delete')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey(
        'menus.id', ondelete='CASCADE'), default=uuid.uuid4)
    menus = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenus', cascade='all,delete')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey(
        'submenus.id', ondelete='CASCADE'), default=uuid.uuid4)
    submenus = relationship('Submenu', back_populates='dishes')
