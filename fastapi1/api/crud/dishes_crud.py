from sqlalchemy.orm import Session

from ...models import models as models
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from .errors.http_error import NotFoundError


def read_dishes(db: Session, menu_id: str, submenu_id: str) -> list[models.Dish]:
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise NotFoundError(detail='menu not found')
    dishes = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id).all()
    return dishes


def create_dish(db: Session, menu_id: str, submenu_id: str, dish_data: DishCreate) -> models.Dish:
    new_dish = models.Dish(**dish_data.model_dump(), submenu_id=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


def get_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str) -> models.Dish:
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise NotFoundError(detail='menu not found')
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).first()
    if not dish:
        raise NotFoundError(detail='dish not found')
    return dish


def patch_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate) -> models.Dish:
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise NotFoundError(detail='menu not found')
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).first()
    if not dish:
        raise NotFoundError(detail='dish not found')
    db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).update(dish_data.model_dump(exclude_unset=True))
    db.commit()
    updated_dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id).first()
    return updated_dish


def delete_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise NotFoundError(detail='menu not found')
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    )
    if not dish.first():
        raise NotFoundError(detail='dish not found')
    dish.delete()
    db.commit()
