from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from pydantic.types import UUID


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int]


class FileRecord(BaseModel):
    id: UUID
    source_id: Optional[str]
    user_id: int
    file_name: str
    type: str
    path: str
    eol: datetime