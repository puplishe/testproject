from fastapi import HTTPException
from sqlalchemy.orm import Session
from ...models import models
from .errors.http_error import NotFoundError
from typing import List, Dict
from .menu_crud import create_menu, read_menu, get_menu_data, delete_menu, get_menu, patch_menu
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate


def read_submenu(menu_id: str, db: Session) -> List[models.Submenu]:
    menu = read_menu(db)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    return submenus

def create_submenu(menu_id: str, submenu: SubmenuCreate, db: Session) -> models.Submenu:
    menu = read_menu(db)
    new_submenu = models.Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu

def delete_submenu(submenu_id: str, db: Session) -> Dict[str, str]:
    get_submenu = db.query(models.Submenu).filter(models.Submenu.id==submenu_id)
    get_submenu.delete()
    db.commit()
    return {'message': 'Submenu deleted successfully'}

def get_submenu(menu_id: str, submenu_id: str, db: Session) -> Dict[str, any]:
    menu_data = get_menu(menu_id, db)
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    dishes_count = len(dishes)
    if not submenu:
        raise NotFoundError(detail="submenu not found")
    response_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'menu_id': submenu.menu_id,
        'dishes_count': dishes_count,
        'dishes': dishes
    }

    return response_data

def patch_submenu(menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate, db: Session) -> models.Submenu:
    menu = read_menu(db)
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id
    ).update(submenu_data.model_dump(exclude_unset=True))
    if submenu == 0:
        raise NotFoundError(detail="submenu not found")
    db.commit()
    updated_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    return updated_submenu