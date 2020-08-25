from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from app.models.models import UserShopRelation, Product


# Shared properties
class ShopBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    address: Optional[str] = None
    staff: List[UserShopRelation] = []
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
