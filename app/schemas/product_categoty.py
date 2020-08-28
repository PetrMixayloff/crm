from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from .product import Product


# Shared properties
class ProductCategoryBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    description: Optional[str] = None
    show_on_store: Optional[bool] = True
    products: Optional[List[Product]] = []


# Properties to receive via API on creation
class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    id: str


# Properties to receive via API on update
class ProductCategoryInDBBase(ProductCategoryBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductCategory(ProductCategoryInDBBase):
    pass
