from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(...)

class PublicItem(BaseModel):
    id:int