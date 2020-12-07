from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .product_raw_relation import ProductRawRelation


# Shared properties
class ProductBase(BaseModel):
    category_id: Union[UUID, str]
    shop_id: Union[UUID, str]
    name: str
    is_active: Optional[bool] = True
    description: Optional[str] = None
    price: Optional[float] = 0
    old_price: Optional[float] = 0
    show_on_store: Optional[bool] = True
    image: Optional[str] = None


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: str


# Properties to receive via API on update
class ProductInDBBase(ProductBase):
    id: UUID
    raw: Optional[List[ProductRawRelation]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    pass
