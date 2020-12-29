from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from .cancelation_record import CancelationRecord, CancelationRecordCreate


# Shared properties
class CancelationBase(BaseModel):
    shop_id: Union[UUID, str]
    number: str
    date: datetime = datetime.utcnow()
    supplier: Optional[str]
    remark: Optional[str]


# Properties to receive via API on creation
class CancelationCreate(CancelationBase):
    records: Optional[List[CancelationRecordCreate]] = []


class CancelationUpdate(CancelationBase):
    id: str


# Properties to receive via API on update
class CancelationInDBBase(CancelationBase):
    id: UUID
    records: Optional[List[CancelationRecord]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cancelation(CancelationInDBBase):
    pass
