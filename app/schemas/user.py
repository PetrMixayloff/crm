from datetime import datetime
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from .shop import UserShop


# Shared properties
class UserBase(BaseModel):
    login: str
    full_name: Optional[str] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_staff: Optional[bool] = True
    shops: List[UserShop] = []


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserUpdate(UserInDBBase):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass
