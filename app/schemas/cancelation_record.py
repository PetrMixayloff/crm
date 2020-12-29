from typing import Optional, Union
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class CancelationRecordBase(BaseModel):
    shop_id: Union[UUID, str]
    cancelation_id: Optional[Union[UUID, str]]
    rawremainsdetail_id: Union[UUID, str]
    quantity: Optional[float] = 0


# Properties to receive via API on creation
class CancelationRecordCreate(CancelationRecordBase):
    pass


class CancelationRecordUpdate(CancelationRecordBase):
    id: str


# Properties to receive via API on update
class CancelationRecordInDBBase(CancelationRecordBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class CancelationRecord(CancelationRecordInDBBase):
    pass
