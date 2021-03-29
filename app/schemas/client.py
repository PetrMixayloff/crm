from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .order import Order


class Address(BaseModel):
    id: Optional[str, UUID] = None
    street: Optional[str] = None
    house: Optional[str] = None
    entrance: Optional[str] = None
    floor: Optional[str] = None
    flat: Optional[str] = None


# Shared properties
class ClientBase(BaseModel):
    shop_id: Union[UUID, str]
    phone: str
    name: str
    sex: Optional[str] = None
    age: Optional[str] = None
    address: Optional[Address] = None
    address_id: Optional[str, UUID] = None
    discount_card: Optional[str] = None
    comment: Optional[str] = None


# Properties to receive via API on creation
class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    id: str


# Properties to receive via API on update
class ClientInDBBase(ClientBase):
    id: UUID
    orders: Optional[List[Order]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Client(ClientInDBBase):
    pass
