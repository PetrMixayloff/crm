from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from .product import Product


# Shared properties
class ProductCategoryBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    description: Optional[str] = None
    products: List[Product] = []


# Properties to receive via API on creation
class ProductCategoryCreate(ProductCategoryBase):
    pass


# Properties to receive via API on update
class ProductCategoryInDBBase(ProductCategoryBase):
    id: UUID

    class Config:
        orm_mode = True


class ProductCategoryUpdate(ProductCategoryInDBBase):
    pass


# Additional properties to return via API
class ProductCategory(ProductCategoryInDBBase):
    pass
