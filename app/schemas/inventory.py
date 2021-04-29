from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone
from .inventory_record import InventoryRecord, InventoryRecordCreate, InventoryRecordUpdate


# Shared properties
class InventoryBase(BaseModel):
    shop_id: Union[UUID, str]
    user_id: Optional[Union[UUID, str]] = None
    number: str
    date: datetime = datetime.utcnow()
    remark: str = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


# Properties to receive via API on creation
class InventoryCreate(InventoryBase):
    records: List[InventoryRecordCreate]


class InventoryUpdate(InventoryBase):
    id: str
    records: List[InventoryRecordUpdate]


# Properties to receive via API on update
class InventoryInDBBase(InventoryBase):
    id: UUID
    records: List[InventoryRecord]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Inventory(InventoryInDBBase):
    pass
