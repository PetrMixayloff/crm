from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.models.models import Product


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


# Properties to receive via API on update
class ProductCategoryInDBBase(ProductCategoryBase):
    id: UUID(as_uuid=True)

    class Config:
        orm_mode = True


class ProductCategoryUpdate(ProductCategoryInDBBase):
    pass


# Additional properties to return via API
class ProductCategory(ProductCategoryInDBBase):
    pass
