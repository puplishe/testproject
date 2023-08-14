from typing import Any

from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from ...cache.cache import RedisCache
from ...models import models
from ...models.schemas.schema_menu import MenusCreate
from ..crud.menu_crud import MenuCrud


class MenuService:
    def __init__(self, backgroundtask: BackgroundTasks, menu_crud: MenuCrud = Depends(), cache: RedisCache = Depends()):
        self._menu_crud = menu_crud
        self.cache = cache
        self.backtask = backgroundtask

    async def create_menu(self, menu: MenusCreate) -> models.Menu:
        self.backtask.add_task(self.cache.delete_cache, '/api/v1/menus/')
        return await self._menu_crud.create_menu(menu)

    async def read_menu(self) -> list[models.Menu]:
        menus = await self._menu_crud.read_menu()
        cache = await self.cache.get_cache('/api/v1/menus/')
        if cache is not None:
            return cache
        else:
            (await self.cache.setcache('/api/v1/menus/', jsonable_encoder(menus)))
        return menus

    async def get_menu(self, menu_id: str) -> dict[str, Any]:
        menu = await self._menu_crud.get_menu(menu_id)
        cache = await self.cache.get_cache(f'/api/v1/menus/{menu_id}')
        if cache is not None:
            return cache
        else:
            (await self.cache.setcache(f'/api/v1/menus/{menu_id}', jsonable_encoder(menu)))

        return menu

    async def patch_menu(self, menu_id: str, menu: MenusCreate) -> dict[str, Any]:
        self.backtask.add_task(self.cache.delete_cache, f'/api/v1/menus/{menu_id}')
        self.backtask.add_task(self.cache.invalidate_cache, '/api/v1/menus')
        return await self._menu_crud.patch_menu(menu_id, menu)

    async def delete_menu(self, menu_id: str) -> None:
        self.backtask.add_task(self.cache.invalidate_cache, '/api/v1/menus')
        return await self._menu_crud.delete_menu(menu_id)

    async def full_menus(self) -> list[dict[str, Any]]:
        return await self._menu_crud.get_full_menus()
