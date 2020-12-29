from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID
from .raw_remains_detail import RawRemainsDetail
from .raw_usage_standards import RawUsageStandards


# Shared properties
class RawBase(BaseModel):
    name: str
    category_id: Union[UUID, str]
    shop_id: Union[UUID, str]
    unit: Optional[str] = None
    remains: Optional[List[RawRemainsDetail]] = []
    reserved: Optional[float] = 0
    per_pack: Optional[int] = 0
    green_signal: Optional[int] = 0
    yellow_signal: Optional[int] = 0
    red_signal: Optional[int] = 0
    description: Optional[str] = None
    image: Optional[str] = None


# Properties to receive via API on creation
class RawCreate(RawBase):
    pass


class RawUpdate(RawBase):
    id: str


# Properties to receive via API on update
class RawInDBBase(RawBase):
    id: UUID
    standards: Optional[List[RawUsageStandards]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Raw(RawInDBBase):
    pass
