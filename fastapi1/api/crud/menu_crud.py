from typing import Any

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...db.database import get_db
from ...models import models
from ...models.schemas.schema_menu import MenusCreate
from .errors.http_error import NotFoundError


class MenuCrud():
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db
        self._model = models.Menu

    async def create_menu(self, menu: MenusCreate) -> models.Menu:
        new_menu = models.Menu(**menu.dict())
        self.db.add(new_menu)
        await self.db.commit()
        return new_menu

    async def read_menu(self) -> list[models.Menu]:
        stmt = select(models.Menu)
        menus = (await self.db.execute(stmt)).scalars().all()
        return menus

    async def get_menu_data(self, menu: models.Menu) -> dict[str, Any]:
        return {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
        }

    async def get_menu(self, menu_id: str) -> dict[str, Any]:
        stmt = select(models.Menu).where(models.Menu.id == menu_id)
        menu = (await self.db.execute(stmt)).scalars().first()
        if menu is None:
            raise NotFoundError(detail='menu not found')
        submenus = (await self.db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu_id))).scalars().all()
        dishes_count = 0
        for submenu in submenus:
            dishes = (await self.db.execute(select(models.Dish).where(models.Dish.submenu_id == submenu.id))).scalars().all()

            dishes_count += len(dishes)

        submenus_count = len(submenus)
        menu_data = {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenus_count,
            'dishes_count': dishes_count
        }

        return menu_data

    async def patch_menu(self, menu_id: str, menu: MenusCreate) -> dict[str, Any]:
        stmt = select(models.Menu).where(models.Menu.id == menu_id)
        menu_data = (await self.db.execute(stmt)).scalars().first()
        if not menu_data:
            raise NotFoundError(detail='menu not found')
        stmt = update(models.Menu).where(models.Menu.id == menu_id).values(menu.dict())
        menu_data = (await self.db.execute(stmt))
        await self.db.commit()
        self.db.refresh(menu_data)

        return await self.get_menu(menu_id)

    async def delete_menu(self, menu_id: str) -> None:
        stmt = delete(models.Menu).where(models.Menu.id == menu_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_full_menus(self) -> list[dict[str, Any]]:
        stmt = select(models.Menu).options(
            selectinload(models.Menu.submenus).selectinload(models.Submenu.dishes)
        )
        result = await self.db.execute(stmt)
        menus = result.scalars().all()

        return menus
