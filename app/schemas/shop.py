from typing import Optional, List
from . import User
from .product import Product
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class ShopBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    staff: List[User] = []
    products: List[Product] = []


class UserShopBase(BaseModel):
    user_id: UUID
    shop_id: UUID
    position: str = None


# Properties to receive via API on creation
class ShopCreate(ShopBase):
    pass


class UserShopCreate(UserShopBase):
    pass


# Properties to receive via API on update
class ShopInDBBase(ShopBase):
    id: UUID

    class Config:
        orm_mode = True


class UserShopInDBBase(UserShopBase):
    id: UUID

    class Config:
        orm_mode = True


class ShopUpdate(ShopInDBBase):
    pass


class UserShopUpdate(UserShopInDBBase):
    pass


# Additional properties to return via API
class Shop(ShopInDBBase):
    pass


class UserShop(ShopInDBBase):
    pass
