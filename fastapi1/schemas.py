from pydantic import BaseModel
from uuid import UUID
class MenusCreate(BaseModel):
    title: str
    description: str

class SubmenuCreate(BaseModel):
    title: str
    description: str

class SubmenuUpdate(BaseModel):
    title: str
    description: str

class DishCreate(BaseModel):
    title: str
    description: str
    price: str

class DishUpdate(BaseModel):
    title: str
    description: str
    price: str