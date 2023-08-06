from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ..services.service_dishes import DishService

router = APIRouter()


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    dish_service = DishService(db)
    return dish_service.read_dishes(menu_id, submenu_id)


@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
def create_dish(menu_id: str, submenu_id: str, dish_data: DishCreate, db: Session = Depends(get_db)):
    dish_service = DishService(db)
    return dish_service.create_dish(menu_id, submenu_id, dish_data)


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    dish_service = DishService(db)
    return dish_service.get_dish(menu_id, submenu_id, dish_id)


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate, db: Session = Depends(get_db)):
    dish_service = DishService(db)
    return dish_service.patch_dish(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    dish_service = DishService(db)
    return dish_service.delete_dish(menu_id, submenu_id, dish_id)
