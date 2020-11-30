from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from .inventory_record import InventoryRecord


# Shared properties
class InventoryBase(BaseModel):
    shop_id: Union[UUID, str]
    user_id: Union[UUID, str]
    number: str
    date: datetime = datetime.utcnow()
    remark: str = None


# Properties to receive via API on creation
class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(InventoryBase):
    id: str


# Properties to receive via API on update
class InventoryInDBBase(InventoryBase):
    id: UUID
    inventory_records: Optional[List[InventoryRecord]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Inventory(InventoryInDBBase):
    pass
