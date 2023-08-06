from typing import Any

from sqlalchemy.orm import Session

from ...models import models
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from .errors.http_error import NotFoundError


def read_submenu(db: Session, menu_id: str) -> list[models.Submenu]:
    submenus = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id).all()
    return submenus


def create_submenu(db: Session, menu_id: str, submenu: SubmenuCreate) -> models.Submenu:
    new_submenu = models.Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    get_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id)
    get_submenu.delete()
    db.commit()
    return get_submenu


def get_submenu(db: Session, menu_id: str, submenu_id: str) -> dict[str, Any]:
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id).first()
    dishes = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id).all()
    dishes_count = len(dishes)
    if not submenu:
        raise NotFoundError(detail='submenu not found')
    response_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'menu_id': submenu.menu_id,
        'dishes_count': dishes_count,
        'dishes': dishes
    }
    return response_data


def patch_submenu(db: Session, menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate) -> models.Submenu:
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id
    ).update(submenu_data.model_dump(exclude_unset=True))
    if submenu == 0:
        raise NotFoundError(detail='submenu not found')
    db.commit()
    updated_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id).first()
    return updated_submenu
