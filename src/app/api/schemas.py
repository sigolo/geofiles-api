from typing import Optional

from pydantic import BaseModel, Field


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int]
