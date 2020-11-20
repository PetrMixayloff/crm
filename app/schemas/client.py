from typing import Optional, List, Union
from pydantic import BaseModel, validator
from uuid import UUID
import re


# Shared properties
class ClientBase(BaseModel):
    shop_id: Union[UUID, str]
    phone: str

    @validator('phone')
    def valid_phone(cls, v):
        if re.match(r'(\+)(7)(9)(\d{9})', v) is None:
            raise ValueError('Not valid phone number')
        return v.title()
    name: str
    address: Optional[str]
    discount: Optional[str] = None
    comment: Optional[str] = None


# Properties to receive via API on creation
class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


# Properties to receive via API on update
class ClientInDBBase(ClientBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Client(ClientInDBBase):
    pass