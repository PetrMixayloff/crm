from datetime import datetime, timezone
from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class RawRemainsDetailBase(BaseModel):
    shop_id: str
    raw_id: str
    invoice_id: Optional[str]
    inventory_id: Optional[str]
    opening_id: Optional[str]
    number: str
    date: datetime = datetime.utcnow()
    price: Optional[float] = 0
    quantity: Optional[float] = 0

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


# Properties to receive via API on creation
class RawRemainsDetailCreate(RawRemainsDetailBase):
    pass


class RawRemainsDetailUpdate(RawRemainsDetailBase):
    id: str


# Properties to receive via API on update
class RawRemainsDetailInDBBase(RawRemainsDetailBase):
    id: UUID
    shop_id: UUID
    raw_id: UUID
    invoice_id: Optional[UUID]
    inventory_id: Optional[UUID]
    opening_id: Optional[UUID]

    class Config:
        orm_mode = True


# Additional properties to return via API
class RawRemainsDetail(RawRemainsDetailInDBBase):
    pass


class RawRemainsDetailsResponse(BaseModel):
    totalCount: int
    data: List[RawRemainsDetail]
