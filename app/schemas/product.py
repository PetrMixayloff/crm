from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.models.models import File


# Shared properties
class ProductBase(BaseModel):
    category_id: UUID(as_uuid=True)
    shop_id: UUID(as_uuid=True)
    name: str
    is_active: Optional[bool] = True
    description: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = 0
    old_price: Optional[float] = 0
    quantity: Optional[int] = 0
    show_on_store: Optional[bool] = True
    images: Optional[List[File]] = []


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    pass


# Properties to receive via API on update
class ProductInDBBase(ProductBase):
    id: UUID(as_uuid=True)

    class Config:
        orm_mode = True


class ProductUpdate(ProductInDBBase):
    pass


# Additional properties to return via API
class Product(ProductInDBBase):
    pass
