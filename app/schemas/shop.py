from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .user import User
from .product import Product


# Shared properties
class ShopBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    address: str


# Properties to receive via API on creation
class ShopCreate(ShopBase):
    pass


class ShopUpdate(ShopBase):
    id: str


# Properties to receive via API on update
class ShopInDBBase(ShopBase):
    id: UUID
    users: Optional[List[User]] = []
    products: Optional[List[Product]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Shop(ShopInDBBase):
    pass
