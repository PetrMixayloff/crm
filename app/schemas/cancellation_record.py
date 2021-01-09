from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID
from .raw_remains_detail import RawRemainsDetail


# Shared properties
class CancellationRecordBase(BaseModel):
    shop_id: Union[UUID, str]
    cancellation_id: Optional[Union[UUID, str]]
    rawremainsdetail_id: Union[UUID, str]
    quantity: Optional[float] = 0
    raw_remains_detail: Optional[List[RawRemainsDetail]] = []


# Properties to receive via API on creation
class CancellationRecordCreate(CancellationRecordBase):
    pass


class CancellationRecordUpdate(CancellationRecordBase):
    id: str


# Properties to receive via API on update
class CancellationRecordInDBBase(CancellationRecordBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class CancellationRecord(CancellationRecordInDBBase):
    pass
