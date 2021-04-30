from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone
from .cancellation_record import CancellationRecord, CancellationRecordCreate


# Shared properties
class CancellationBase(BaseModel):
    shop_id: Union[UUID, str]
    number: Optional[int] = None
    date: datetime = datetime.utcnow()
    reason: Optional[str]
    remark: Optional[str]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


# Properties to receive via API on creation
class CancellationCreate(CancellationBase):
    records: List[CancellationRecordCreate]


class CancellationUpdate(CancellationBase):
    id: str


# Properties to receive via API on update
class CancellationInDBBase(CancellationBase):
    id: UUID
    records: List[CancellationRecord]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cancellation(CancellationInDBBase):
    pass
