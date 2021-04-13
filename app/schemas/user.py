from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, validator
from .permissions import Permissions
import re


# Shared properties
class UserBase(BaseModel):
    phone: str

    @validator('phone')
    def valid_phone(cls, v):
        if re.match(r'(\+)(7)(9)(\d{9})', v) is None:
            raise ValueError('Not valid phone number')
        return v.title()

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


class UserLogin(UserBase):
    password: str


class SuperUserCreate(UserLogin):
    is_superuser: bool = True


class AdminCreate(UserLogin):
    full_name: str
    position: Optional[str] = 'Владелец'
    is_staff: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "full_name": "admin",
                "password": "admin"
            }
        }


# Properties to receive via API on creation
class UserCreate(UserLogin):
    full_name: str
    position: str
    shop_id: str
    description: Optional[str] = None


class UserUpdate(UserCreate):
    id: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: UUID
    full_name: str
    position: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    shop_id: UUID
    permissions: Optional[Permissions] = None
    last_login: Optional[datetime] = None
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = True

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str


class UsersResponse(BaseModel):
    totalCount: int
    data: List[User]
