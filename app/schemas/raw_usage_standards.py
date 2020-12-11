from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class RawUsageStandardsBase(BaseModel):
    shop_id: Union[UUID, str]
    name: Optional[str]
    quantity: Optional[float] = 0


# Properties to receive via API on creation
class RawUsageStandardsCreate(RawUsageStandardsBase):
    raw_id: str


class RawUsageStandardsUpdate(RawUsageStandardsBase):
    raw_id: str
    id: str


# Properties to receive via API on update
class RawUsageStandardsInDBBase(RawUsageStandardsBase):
    id: UUID
    raw_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class RawUsageStandards(RawUsageStandardsInDBBase):
    pass
