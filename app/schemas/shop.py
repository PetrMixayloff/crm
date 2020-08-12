from typing import Optional, List
from .user import User
from .product import Product
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID


# Shared properties
class ShopBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    staff: List[User] = []
    products: List[Product] = []


# Properties to receive via API on creation
class ShopCreate(ShopBase):
    pass


# Properties to receive via API on update
class ShopInDBBase(ShopBase):
    id: UUID

    class Config:
        orm_mode = True


class ShopUpdate(ShopInDBBase):
    pass


# Additional properties to return via API
class Shop(ShopInDBBase):
    pass
