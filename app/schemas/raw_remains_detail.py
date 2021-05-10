from datetime import datetime, timezone
from typing import Optional, Union, List
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class RawRemainsDetailBase(BaseModel):
    shop_id: Union[UUID, str]
    raw_id: Union[UUID, str]
    invoice_id: Optional[Union[UUID, str]]
    inventory_id: Optional[Union[UUID, str]]
    invoice: bool
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

    class Config:
        orm_mode = True


# Additional properties to return via API
class RawRemainsDetail(RawRemainsDetailInDBBase):
    pass
