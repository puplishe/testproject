import re

import pandas as pd

from ..api.crud.dishes_crud import DishesCrud
from ..api.crud.menu_crud import MenuCrud
from ..api.crud.submenu_crud import SubmenuCrud
from ..models.schemas.schema_dish import DishCreate, DishUpdate
from ..models.schemas.schema_menu import MenusCreate, MenusUpdate
from ..models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate


class ExcelParser():
    def __init__(self, menu_service: MenuCrud, submenu_service: SubmenuCrud, dish_service: DishesCrud) -> None:
        self.__menu_servise = menu_service
        self.__submenu_service = submenu_service
        self.__dish_service = dish_service

    async def parser(self):
        df = pd.read_excel('fastapi1/admin/Menu.xlsx', header=None)
        uuid4_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$', re.I)
        current_menu = None
        current_submenu = None
        current_dish = None
        menu_uuid = []
        submenu_uuid = []
        dish_uuid = []
        menu_db_uuid = []
        submenu_db_uuid = []
        dish_db_uuid = []
        for index, row in df.iterrows():
            if pd.notna(row[0]):
                if isinstance(row[0], (int, float)):

                    menu = MenusCreate(title=row[1], description=row[2])
                    current_menu = await self.__menu_servise.create_menu(menu=menu)
                    menu_uuid.append(current_menu.id)
                    df.at[index, 0] = current_menu.id
                    current_menu_id = current_menu.id
                elif isinstance(row[0], str) and uuid4_pattern.match(row[0]):

                    uuid = row[0]

                    menu = MenusUpdate(title=row[1], description=row[2])
                    current_menu = await self.__menu_servise.patch_menu(uuid, menu=menu)
                    menu_uuid.append(current_menu['id'])
                    current_menu_id = current_menu['id']

            if pd.notna(row[1]):
                if isinstance(row[1], (float, int)):
                    submenu = SubmenuCreate(title=row[2], description=row[3])
                    current_submenu = await self.__submenu_service.create_submenu(menu_id=current_menu_id, submenu=submenu)
                    submenu_uuid.append(current_submenu.id)

                    df.at[index, 1] = current_submenu.id
                    current_submenu_id = current_submenu.id
                elif isinstance(row[1], str) and uuid4_pattern.match(row[1]):

                    submenu = SubmenuUpdate(title=row[2], description=row[3])
                    current_submenu = await self.__submenu_service.patch_submenu(row[1], submenu_data=submenu)
                    submenu_uuid.append(current_submenu.id)
                    current_submenu_id = current_submenu.id
            if pd.notna(row[2]):
                if isinstance(row[2], (float, int)):
                    dish = DishCreate(title=row[3], description=row[4], price=row[5])
                    current_dish = await self.__dish_service.create_dish(current_menu_id, current_submenu_id, dish_data=dish)
                    dish_uuid.append(current_dish.id)
                    df.at[index, 2] = current_dish.id
                    current_dish_id = current_dish.id
                elif isinstance(row[2], str) and uuid4_pattern.match(row[2]):
                    print(row[2])
                    print('1')
                    dish = DishUpdate(title=row[3], description=row[4], price=row[5])
                    current_dish = await self.__dish_service.patch_dish(row[2], dish_data=dish)
                    df.at[index, 2] = current_dish.id
                    current_dish_id = current_dish.id
                    dish_uuid.append(current_dish_id)
        df.to_excel('fastapi1/admin/Menu.xlsx', index=False, header=None)
        print(1)
        response = await self.__menu_servise.read_menu()
        for menu in response:
            menu_db_uuid.append(menu.id)
        for uuid in menu_db_uuid:

            response = await self.__submenu_service.read_submenu(uuid)
            for submenu in response:

                submenu_db_uuid.append(submenu.id)
        for id in menu_db_uuid:
            for uuid in submenu_db_uuid:
                response = await self.__dish_service.read_dishes(id, uuid)
                if response != []:
                    for dish in response:
                        dish_db_uuid.append(dish.id)
        delete_dish = [dish for dish in dish_db_uuid if dish not in dish_uuid]
        if delete_dish:
            for id in delete_dish:
                print(id)
                await self.__dish_service.delete_dish(id)
        delete_menu = [menu for menu in menu_db_uuid if menu not in menu_uuid]
        if delete_menu:
            for id in delete_menu:
                await self.__menu_servise.delete_menu(id)
        delete_submenu = [submenu for submenu in submenu_db_uuid if submenu not in submenu_uuid]
        if delete_submenu:
            for id in delete_submenu:
                await self.__submenu_service.delete_submenu(id)
            print('deleted')
