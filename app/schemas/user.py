from datetime import datetime
from typing import Optional, List, Union
from uuid import UUID
from pydantic import BaseModel, validator
import re


# Shared properties
class UserBase(BaseModel):
    phone: str
    shop_id: Union[UUID, str, None] = None
    full_name: Optional[str] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = True

    @validator('phone')
    def valid_phone(cls, v):
        if re.match(r'(\+)(7)(\s)?(9)(\d{2})(\s)?(\d{7})', v) is not None:
            raise ValueError('Not valid phone number')
        return v.title()


class UserLogin(BaseModel):
    login: str
    password: str


class AdminCreate(UserLogin):
    full_name: str
    phone_number: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: str
    password: Optional[str] = None


# Properties to receive via API on update
class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
