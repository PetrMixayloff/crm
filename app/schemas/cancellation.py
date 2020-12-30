from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from .cancellation_record import CancellationRecord, CancellationRecordCreate


# Shared properties
class CancellationBase(BaseModel):
    shop_id: Union[UUID, str]
    number: str
    date: datetime = datetime.utcnow()
    supplier: Optional[str]
    remark: Optional[str]


# Properties to receive via API on creation
class CancellationCreate(CancellationBase):
    records: Optional[List[CancellationRecordCreate]] = []


class CancellationUpdate(CancellationBase):
    id: str


# Properties to receive via API on update
class CancellationInDBBase(CancellationBase):
    id: UUID
    records: Optional[List[CancellationRecord]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cancellation(CancellationInDBBase):
    pass
