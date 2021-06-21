from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from .raw_remains_detail import RawRemainsDetail


# Shared properties
class RawBase(BaseModel):
    category_id: str
    piece_raw_id: Optional[str] = None
    shop_id: str
    name: str
    article_number: Optional[str] = None
    manufacturer: Optional[str] = None
    unit: str
    piece_unit: Optional[str] = None
    per_pack: Optional[float] = None
    helium_consumption: Optional[float] = 0
    description: Optional[str] = None
    image: Optional[str] = None
    yellow_label: Optional[float] = 0
    red_label: Optional[float] = 0
    quantity: Optional[float] = 0
    available_quantity: Optional[float] = 0
    reserved: Optional[float] = 0


# Properties to receive via API on creation
class RawCreate(RawBase):
    pass


class RawUpdate(RawBase):
    id: str


# Properties to receive via API on update
class RawInDBBase(RawBase):
    id: UUID
    category_id: UUID
    piece_raw_id: Optional[UUID] = None
    shop_id: UUID
    remains: Optional[List[RawRemainsDetail]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Raw(RawInDBBase):
    pass


class RawResponse(BaseModel):
    totalCount: int
    data: List[Raw]
