from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID
from .raw_remains_detail import RawRemainsDetail
from .raw_usage_standards import RawUsageStandards


# Shared properties
class RawBase(BaseModel):
    category_id: Union[UUID, str]
    piece_raw_id: Optional[Union[UUID, str]] = None
    shop_id: Union[UUID, str]
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
    standards: Optional[List[RawUsageStandards]] = []
    remains: Optional[List[RawRemainsDetail]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Raw(RawInDBBase):
    pass
