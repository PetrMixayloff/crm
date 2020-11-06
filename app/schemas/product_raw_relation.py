from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class ProductRawRelationBase(BaseModel):
    product_id: Optional[Union[UUID, str]] = None
    raw_id: Union[UUID, str]
    quantity: Optional[int] = 0


# Properties to receive via API on creation
class ProductRawRelationCreate(ProductRawRelationBase):
    pass


class ProductRawRelationUpdate(ProductRawRelationBase):
    id: str


# Properties to receive via API on update
class ProductRawRelationInDBBase(ProductRawRelationBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductRawRelation(ProductRawRelationInDBBase):
    pass
