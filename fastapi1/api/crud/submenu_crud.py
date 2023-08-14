from typing import Any

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.database import get_db
from ...models import models
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from .errors.http_error import NotFoundError


class SubmenuCrud():
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def get_submenu_by_id(self, submenu_id: str) -> dict[str, Any]:
        stmt = select(models.Submenu).where(models.Submenu.id == submenu_id)
        submenus = (await self.db.execute(stmt)).scalars().first()
        return submenus

    async def read_submenu(self, menu_id: str) -> list[models.Submenu]:
        stmt = select(models.Submenu).where(models.Submenu.menu_id == menu_id)
        submenus = (await self.db.execute(stmt))
        return submenus.scalars().all()

    async def create_submenu(self, menu_id: str, submenu: SubmenuCreate) -> models.Submenu:
        new_submenu = models.Submenu(**submenu.dict(), menu_id=menu_id)
        self.db.add(new_submenu)
        await self.db.commit()
        return new_submenu

    async def delete_submenu(self, submenu_id: str) -> None:
        stmt = delete(models.Submenu).where(models.Submenu.id == submenu_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_submenu(self, menu_id: str, submenu_id: str) -> dict[str, Any]:
        stmt = select(models.Submenu).where(models.Submenu.id == submenu_id)
        submenus = (await self.db.execute(stmt)).scalars().first()
        if submenus is None:
            raise NotFoundError(detail='submenu not found')
        stmt = select(models.Dish).where(models.Dish.submenu_id == submenu_id)
        dishes = (await self.db.execute(stmt)).scalars().all()
        dishes_count = len(dishes)
        submenu_data = {
            'id': submenus.id,
            'title': submenus.title,
            'description': submenus.description,
            'dishes_count': dishes_count
        }
        return submenu_data

    async def patch_submenu(self, submenu_id: str, submenu_data: SubmenuUpdate) -> dict[str, Any]:
        stmt = update(models.Submenu).where(models.Submenu.id == submenu_id).values(submenu_data.dict())
        submenu_data = (await self.db.execute(stmt))
        await self.db.commit()
        self.db.refresh(submenu_data)
        return await self.get_submenu_by_id(submenu_id)
