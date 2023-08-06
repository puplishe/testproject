from typing import Any

from sqlalchemy.orm import Session

from ...cache.cache import cache, cached_with_redis
from ...cache.repository.cache_dishes import invalidate_dish_cache
from ...models import models
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ..crud.dishes_crud import create_dish as db_create_dish
from ..crud.dishes_crud import delete_dish as db_delete_dish
from ..crud.dishes_crud import get_dish as db_get_dish
from ..crud.dishes_crud import patch_dish as db_patch_dish
from ..crud.dishes_crud import read_dishes as db_read_dishes


class DishService:
    def __init__(self, db: Session):
        self.db = db

    def read_dishes(self, menu_id: str, submenu_id: str) -> list[models.Dish]:
        @cached_with_redis(cache, key_func=lambda: f'{menu_id}:{submenu_id}:dishes')
        def _read_dishes():
            dishes = db_read_dishes(self.db, menu_id, submenu_id)
            return dishes
        return _read_dishes()

    def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate) -> models.Dish:
        new_dish = db_create_dish(self.db, menu_id, submenu_id, dish_data)
        invalidate_dish_cache(menu_id, submenu_id, str(new_dish.id))
        return new_dish

    def get_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dict[str, Any]:
        @cached_with_redis(cache, key_func=lambda: f'{menu_id}:{submenu_id}:dishes:{dish_id}')
        def _get_dish():
            dish = db_get_dish(self.db, menu_id, submenu_id, dish_id)
            return dish
        return _get_dish()

    def patch_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate) -> models.Dish:
        updated_dish = db_patch_dish(
            self.db, menu_id, submenu_id, dish_id, dish_data)
        invalidate_dish_cache(menu_id, submenu_id, dish_id)
        return updated_dish

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        invalidate_dish_cache(menu_id, submenu_id, dish_id)
        return db_delete_dish(self.db, menu_id, submenu_id, dish_id)
