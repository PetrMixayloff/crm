from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .product import Product


# Shared properties
class ProductCategoryBase(BaseModel):
    name: str
    shop_id: Union[str, UUID]
    is_active: Optional[bool] = True
    description: Optional[str] = None
    show_on_store: Optional[bool] = True


# Properties to receive via API on creation
class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    pass


# Properties to receive via API on update
class ProductCategoryInDBBase(ProductCategoryBase):
    id: UUID
    products: Optional[List[Product]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductCategory(ProductCategoryInDBBase):
    pass
