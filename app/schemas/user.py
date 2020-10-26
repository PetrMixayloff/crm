from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from .file import File
import re


# Shared properties
class UserBase(BaseModel):
    phone: str

    @validator('phone')
    def valid_phone(cls, v):
        if re.match(r'(\+)(7)(\s)?(9)(\d{2})(\s)?(\d{7})', v) is not None:
            raise ValueError('Not valid phone number')
        return v.title()


class UserLogin(UserBase):
    password: str


class SuperUserCreate(UserLogin):
    is_superuser: bool = True


class AdminCreate(UserLogin):
    full_name: str
    position: str = 'Владелец'
    is_staff: bool = False


# Properties to receive via API on creation
class UserCreate(UserLogin):
    full_name: str
    position: str
    shop_id: str
    description: Optional[str] = None
    avatar: Optional[File] = None


class UserUpdate(UserCreate):
    id: str
    password: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserInDBBase(UserCreate):
    id: UUID
    shop_id: UUID
    last_login: Optional[datetime] = None
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = True

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
