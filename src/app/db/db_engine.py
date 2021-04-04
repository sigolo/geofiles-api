import os

from sqlalchemy import (create_engine)

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")
# SQLAlchemy
engine = create_engine(DATABASE_URL)
# databases query builder
database = Database(DATABASE_URL)