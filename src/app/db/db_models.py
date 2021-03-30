from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.sql import expression

metadata = MetaData()

Items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

