from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID


class Address(BaseModel):
    id: Optional[Union[str, UUID]] = None
    street: Optional[str] = None
    house: Optional[str] = None
    entrance: Optional[str] = None
    floor: Optional[str] = None
    flat: Optional[str] = None


class AddressInDB(Address):
    id: UUID

    class Config:
        orm_mode = True


# Shared properties
class ClientBase(BaseModel):
    shop_id: Union[UUID, str]
    phone: str
    name: str
    sex: Optional[str] = None
    age: Optional[str] = None
    address: Optional[Address] = None
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
    address: Optional[AddressInDB] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Client(ClientInDBBase):
    pass
