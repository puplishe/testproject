from typing import Any

from sqlalchemy.orm import Session

from ...models import models
from ...models.schemas.schema_menu import MenusCreate
from .errors.http_error import NotFoundError
from .submenu_crud import read_submenu


def create_menu(db: Session, menu: MenusCreate) -> models.Menu:
    new_menu = models.Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def read_menu(db: Session) -> list[models.Menu]:
    menus = db.query(models.Menu).all()
    return menus


def get_menu_data(menu: models.Menu, submenus: list[models.Submenu]) -> dict[str, Any]:
    submenus_count = len(submenus)
    dishes_count = sum(len(submenu.dishes) for submenu in submenus)

    return {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description,
        'submenus_count': submenus_count,
        'dishes_count': dishes_count,
        'submenus': submenus
    }


def get_menu(db: Session, menu_id: str) -> dict[str, Any]:
    menu = db.query(models.Menu).get(menu_id)
    if not menu:
        raise NotFoundError(detail='menu not found')

    submenus = read_submenu(db, menu_id)
    return get_menu_data(menu, submenus)


def patch_menu(db: Session, menu_id: str, menu: MenusCreate) -> models.Menu:
    menu_data = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu_data:
        raise NotFoundError(detail='menu not found')

    menu_query = db.query(models.Menu).filter(models.Menu.id == menu_id)
    menu_query.update(menu.model_dump(), synchronize_session=False)
    db.commit()
    updated_menu = menu_query.first()
    return updated_menu


def delete_menu(db: Session, menu_id: str):
    menu_query = db.query(models.Menu).filter(models.Menu.id == menu_id)
    menu_query.delete()
    db.commit()
