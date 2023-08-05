from typing import List
from sqlalchemy.orm import Session
from ...models import models as models
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from .errors.http_error import NotFoundError
from .menu_crud import read_menu
from .submenu_crud import read_submenu

def read_dishes(menu_id: str, submenu_id: str, db: Session) -> List[models.Dish]:
    menu = read_menu(db)
    submenu = read_submenu(menu_id, db)
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    return dishes

def create_dish(menu_id: str, submenu_id: str, dish_data: DishCreate, db: Session) -> models.Dish:
    new_dish = models.Dish(**dish_data.model_dump(), submenu_id=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish

def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session) -> models.Dish:
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).first()
    if not dish:
        raise NotFoundError(detail='dish not found')
    return dish

def patch_dish(menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate, db: Session) -> models.Dish:
    update_dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).update(dish_data.model_dump(exclude_unset=True))
    if update_dish == 0:
        raise NotFoundError(detail='dish not found')
    db.commit()
    updated_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    return updated_dish

def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session) -> models.Dish:
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    )
    dish.delete()
    db.commit()
    return dish
