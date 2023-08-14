from typing import Any

from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder

from ...cache.cache import RedisCache
from ...models import models
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ..crud.submenu_crud import SubmenuCrud


class SubmenuService:
    def __init__(self, backgroundtask: BackgroundTasks, submenucrud: SubmenuCrud = Depends(), cache: RedisCache = Depends()):
        self._submenu_crud = submenucrud
        self.cache = cache
        self.backtast = backgroundtask

    async def read_submenu(self, menu_id: str) -> list[models.Submenu]:

        submenus = await self._submenu_crud.read_submenu(menu_id=menu_id)
        cache = await self.cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/')
        if cache is not None:

            return cache
        else:

            await self.cache.setcache(f'/api/v1/menus/{menu_id}/submenus/', jsonable_encoder(submenus))
            return submenus

    async def create_submenu(self, menu_id: str, submenu: SubmenuCreate) -> models.Submenu:
        new_submenu = await self._submenu_crud.create_submenu(menu_id=menu_id, submenu=submenu)
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}')
        return new_submenu

    async def delete_submenu(self, menu_id: str, submenu_id: str) -> None:
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}')
        return await self._submenu_crud.delete_submenu(submenu_id)

    async def get_submenu(self, menu_id: str, submenu_id: str) -> dict[str, Any]:

        submenu_data = await self._submenu_crud.get_submenu(
            menu_id=menu_id, submenu_id=submenu_id)
        cache = await self.cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        if cache:
            return cache
        else:
            await self.cache.setcache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', jsonable_encoder(submenu_data))
        return submenu_data

    async def patch_submenu(self, menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate) -> dict[str, Any]:
        self.backtast.add_task(self.cache.delete_cache, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        self.backtast.add_task(self.cache.invalidate_cache, f'/api/v1/menus/{menu_id}')
        updated_submenu = await self._submenu_crud.patch_submenu(submenu_id=submenu_id, submenu_data=submenu_data)
        return updated_submenu
