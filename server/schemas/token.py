from typing import Optional
from pydantic import BaseModel
from schemas.user import UserRead


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional[UserRead] = None