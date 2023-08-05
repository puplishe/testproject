from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import dishes_crud
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ...db.database import get_db

router = APIRouter()

@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return dishes_crud.read_dishes(menu_id, submenu_id, db)

@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
def create_dish(menu_id: str, submenu_id: str, dish_data: DishCreate, db: Session = Depends(get_db)):
    return dishes_crud.create_dish(menu_id, submenu_id, dish_data, db)

@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return dishes_crud.get_dish(menu_id, submenu_id, dish_id, db)

@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate, db: Session = Depends(get_db)):
    return dishes_crud.patch_dish(menu_id, submenu_id, dish_id, dish_data, db)

@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    return dishes_crud.delete_dish(menu_id, submenu_id, dish_id, db)
