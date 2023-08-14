from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from ...models.schemas.schema_dish import DishCreate, DishUpdate
from ..services.service_dishes import DishService

router = APIRouter()


@cbv(router)
class DishesRouter:
    __dish_service: DishService = Depends()

    @router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes')
    async def read_dishes(self, menu_id: str, submenu_id: str):
        return await self.__dish_service.read_dishes(menu_id, submenu_id)

    @router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=201)
    async def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate):
        return await self.__dish_service.create_dish(menu_id, submenu_id, dish_data)

    @router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def get_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        return await self.__dish_service.get_dish(menu_id, submenu_id, dish_id)

    @router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def patch_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate):
        return await self.__dish_service.patch_dish(menu_id, submenu_id, dish_id, dish_data)

    @router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    async def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str):
        return await self.__dish_service.delete_dish(menu_id, submenu_id, dish_id)
