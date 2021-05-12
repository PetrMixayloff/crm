from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone


# Shared properties
class OpeningBase(BaseModel):
    shop_id: str
    number: Optional[int] = None
    date: datetime = datetime.utcnow()
    remark: Optional[str]
    raw_remains_details_id: str
    raw_id: str

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


# Properties to receive via API on creation
class OpeningCreate(OpeningBase):
    pass


class OpeningUpdate(OpeningBase):
    id: str


# Properties to receive via API on update
class OpeningInDBBase(OpeningBase):
    id: UUID
    shop_id: UUID
    number: int
    date: datetime = datetime.utcnow()
    remark: Optional[str]
    raw_remains_details_id: UUID
    raw_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Opening(OpeningInDBBase):
    pass


class OpeningResponse(BaseModel):
    totalCount: int
    data: List[Opening]
