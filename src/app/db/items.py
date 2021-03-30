from fastapi.security import OAuth2PasswordRequestForm

from ..api.schemas import Item as ItemSchema
from .db_models import Items as ItemsTable
from .db_engine import database


async def create(item: ItemSchema):
    query = ItemsTable.insert().values(name=item.name)
    return await database.execute(query=query)


async def get_one(id: int):
    query = ItemsTable.select().where(id == ItemsTable.c.id)
    return await database.fetch_one(query=query)