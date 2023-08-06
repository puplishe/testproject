from pydantic import BaseModel


class BaseSchema(BaseModel):
    title: str
    description: str
