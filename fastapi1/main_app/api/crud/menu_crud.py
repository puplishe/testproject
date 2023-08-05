from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from ...models.schemas.schema_menu import MenusCreate, MenusUpdate
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ...models import models
from .errors.http_error import NotFoundError

from fastapi.responses import JSONResponse
import uvicorn



def create_menu(menu: MenusCreate, db: Session):
    new_menu = models.Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

def read_menu(db: Session):
    get_menus = db.query(models.Menu).all()
    return get_menus

def get_menu_data(menu, submenus):
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

def get_menu(menu_id: str, db: Session):
    menu = db.query(models.Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    return get_menu_data(menu, submenus)

def patch_menu(menu_id: str, menu: MenusCreate, db: Session):
    get_menu = db.query(models.Menu).filter(models.Menu.id == menu_id)
    get_menu.first()
    get_menu.update(menu.model_dump(), synchronize_session=False)
    db.commit()
    return get_menu.first()

def delete_menu(menu_id: str, db: Session):
    get_menu = db.query(models.Menu).filter(models.Menu.id == menu_id)
    get_menu.delete()
    db.commit()
    return get_menu