from datetime import datetime
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    login: str
    shop_id: Optional[UUID(as_uuid=True)] = None
    full_name: Optional[str] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = True


class UserLogin(BaseModel):
    username: str
    password: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: UUID(as_uuid=True)

    class Config:
        orm_mode = True


class UserUpdate(UserInDBBase):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass
