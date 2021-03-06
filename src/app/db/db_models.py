from sqlalchemy import MetaData, Table, Column, Integer, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

metadata = MetaData()

Files = Table(
    "files",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4()),
    Column("source_id", UUID, default=None),
    Column("user_id", Integer),
    Column("file_name", String),
    Column("type", Enum("SHP", "CAD", "CSV", "GEOJSON", create_type=False, name="allowed_format")),
    Column("path", String(255)),
    Column("eol", DateTime, default=func.now())
)

