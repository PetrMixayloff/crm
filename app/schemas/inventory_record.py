from typing import Union
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class InventoryRecordBase(BaseModel):
    raw_id: Union[UUID, str]
    quantity: float
    old_quantity: float


# Properties to receive via API on creation
class InventoryRecordCreate(InventoryRecordBase):
    pass


# Properties to receive via API on update
class InventoryRecordInDBBase(InventoryRecordBase):
    id: UUID
    inventory_id: UUID
    shop_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class InventoryRecord(InventoryRecordInDBBase):
    pass
