from typing import Any

from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from ...cache.cache import RedisCache
from ...models import models
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ..crud.dishes_crud import DishesCrud


class DishService:
    def __init__(self, backgroundtask: BackgroundTasks, dishcrud: DishesCrud = Depends(), cache: RedisCache = Depends()):
        self._dish_crud = dishcrud
        self.cache = cache
        self.backtast = backgroundtask

    async def read_dishes(self, menu_id: str, submenu_id: str) -> list[models.Dish]:
        dishes = await self._dish_crud.read_dishes(menu_id, submenu_id)
        cache = await self.cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
        if cache is not None:
            dishes = cache
        else:
            await self.cache.setcache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', jsonable_encoder(dishes))
        return dishes

    async def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate) -> models.Dish:
        new_dish = await self._dish_crud.create_dish(menu_id, submenu_id, dish_data)
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        return new_dish

    async def get_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dict[str, Any]:
        dish = await self._dish_crud.get_dish(menu_id, submenu_id, dish_id)
        cache = await self.cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        if cache:
            return cache
        else:
            await self.cache.setcache(
                f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', jsonable_encoder(dish))
        return dish

    async def patch_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate) -> models.Dish:
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}')
        self.backtast.add_task(self.cache.delete_cache,
                               f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        updated_dish = await self._dish_crud.patch_dish(dish_id, dish_data)
        return updated_dish

    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}')
        return await self._dish_crud.delete_dish(dish_id)
