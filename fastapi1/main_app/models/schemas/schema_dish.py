from .base import BaseSchema


class DishCreate(BaseSchema):
    price: str


class DishUpdate(BaseSchema):
    price: str