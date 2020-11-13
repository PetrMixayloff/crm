from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
import re


# Shared properties
class UserBase(BaseModel):
    phone: str

    @validator('phone')
    def valid_phone(cls, v):
        if re.match(r'(\+)(7)(9)(\d{9})', v) is None:
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


class UserUpdate(UserCreate):
    id: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: Optional[UUID] = None
    full_name: str
    position: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    shop_id: Optional[UUID] = None
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
