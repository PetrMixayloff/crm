from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from .file import File


# Shared properties
class ProductBase(BaseModel):
    name: str
    is_active: Optional[bool] = True
    description: Optional[str] = None
    url: Optional[str] = None
    category_id: UUID
    images: List[File] = []


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    pass


# Properties to receive via API on update
class ProductInDBBase(ProductBase):
    id: UUID

    class Config:
        orm_mode = True


class ProductUpdate(ProductInDBBase):
    pass


# Additional properties to return via API
class Product(ProductInDBBase):
    pass
