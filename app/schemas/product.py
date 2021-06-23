from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .product_raw_relation import ProductRawRelation, ProductRawRelationCreate, ProductRawRelationUpdate


class ProductSetRelationCreateUpdate(BaseModel):
    product_id: str
    product_set_id: Optional[str] = None
    quantity: float


class ProductSetRelation(ProductSetRelationCreateUpdate):
    product_id: UUID
    product_set_id: UUID


# Shared properties
class ProductBase(BaseModel):
    category_id: str
    shop_id: str
    name: str
    base: Optional[bool] = True
    is_active: Optional[bool] = True
    description: Optional[str] = None
    price: Optional[float] = 0
    old_price: Optional[float] = 0
    show_on_store: Optional[bool] = True
    image: Optional[str] = None
    product_set_id: Optional[str] = None


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    raw: Optional[List[ProductRawRelationCreate]] = []
    products: Optional[List[ProductSetRelationCreateUpdate]] = []


class ProductUpdate(ProductBase):
    id: str
    raw: Optional[List[Union[ProductRawRelationUpdate, ProductRawRelationCreate]]] = []
    products: Optional[List[ProductSetRelationCreateUpdate]] = []


# Properties to receive via API on update
class ProductInDBBase(ProductBase):
    id: UUID
    category_id: UUID
    shop_id: UUID
    product_set_id: Optional[UUID] = None
    raw: Optional[List[ProductRawRelation]] = []
    products: Optional[List[ProductSetRelation]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    pass


class ProductResponse(BaseModel):
    totalCount: int
    data: List[Product]
