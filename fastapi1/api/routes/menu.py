from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from ...models.schemas.schema_menu import MenusCreate
from ..services.service_menu import MenuService

router = APIRouter()


@cbv(router)
class MenuRouter:

    __menu_service: MenuService = Depends()

    @router.post('/menus', status_code=201)
    async def create_menu(self, menu: MenusCreate):

        return await self.__menu_service.create_menu(menu)

    @router.get('/menus')
    async def read_menu(self):

        return await self.__menu_service.read_menu()

    @router.get('/menus/{menu_id}')
    async def get_menu(self, menu_id: str):

        return await self.__menu_service.get_menu(menu_id)

    @router.patch('/menus/{menu_id}')
    async def patch_menu(self, menu_id: str, menu: MenusCreate):

        return await self.__menu_service.patch_menu(menu_id, menu)

    @router.delete('/menus/{menu_id}')
    async def delete_menu(self, menu_id: str):

        return await self.__menu_service.delete_menu(menu_id)

    @router.get(
        '/menus_info/',
        summary='Get full info about menus including dishes,submenus',
        description='To get full info send a GET request, '
                    'the response comes according to the changes in the administrators excel file'
    )
    async def get_all_info_router(self):
        return await self.__menu_service.full_menus()
