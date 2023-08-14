from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ..services.service_submenu import SubmenuService

router = APIRouter()


@cbv(router)
class SubmenuRouter:

    __submenu_service: SubmenuService = Depends()

    @router.get('/menus/{menu_id}/submenus')
    async def read_submenu(self, menu_id: str):
        return await self.__submenu_service.read_submenu(menu_id)

    @router.post('/menus/{menu_id}/submenus', status_code=201)
    async def create_submenu(self, menu_id: str, submenu: SubmenuCreate):
        return await self.__submenu_service.create_submenu(menu_id, submenu)

    @router.delete('/menus/{menu_id}/submenus/{submenu_id}')
    async def delete_submenu(self, menu_id: str, submenu_id: str):
        return await self.__submenu_service.delete_submenu(menu_id, submenu_id)

    @router.get('/menus/{menu_id}/submenus/{submenu_id}')
    async def get_submenu(self, menu_id: str, submenu_id: str):
        return await self.__submenu_service.get_submenu(menu_id, submenu_id)

    @router.patch('/menus/{menu_id}/submenus/{submenu_id}')
    async def patch_submenu(self, menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate):
        return await self.__submenu_service.patch_submenu(menu_id, submenu_id, submenu_data)
