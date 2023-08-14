from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.database import get_db
from ...models import models as models
from ...models.schemas.schema_dish import DishCreate, DishUpdate
from .errors.http_error import NotFoundError


class DishesCrud:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def get_dish_by_id(self, dish_id: str) -> models.Dish:
        """Get dish by id"""
        dish = (await self.db.execute(select(models.Dish).where(models.Dish.id == dish_id))).scalars().first()
        return dish

    async def read_dishes(self, menu_id: str, submenu_id: str) -> list[models.Dish]:
        stmt = select(models.Dish).where(models.Dish.submenu_id == submenu_id)
        dishes = (await self.db.execute(stmt)).scalars().all()

        return dishes

    async def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate) -> models.Dish:
        dish = models.Dish(**dish_data.dict(), submenu_id=submenu_id)
        self.db.add(dish)
        await self.db.commit()
        return dish

    async def get_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> models.Dish:
        stmt = select(models.Dish).where(models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id)
        dish = (await self.db.execute(stmt)).scalars().first()
        if dish is None:
            raise NotFoundError(detail='dish not found')
        return dish

    async def patch_dish(self, dish_id: str, dish_data: DishUpdate) -> models.Dish:
        stmt = update(models.Dish).where(models.Dish.id == dish_id).values(dish_data.dict())
        updated_data = (await self.db.execute(stmt))
        await self.db.commit()
        self.db.refresh(updated_data)
        return await self.get_dish_by_id(dish_id)

    async def delete_dish(self, dish_id: str) -> None:
        stmt = delete(models.Dish).where(models.Dish.id == dish_id)
        await self.db.execute(stmt)
        await self.db.commit()
