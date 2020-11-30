from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class InventoryRecordBase(BaseModel):
    shop_id: Union[UUID, str]
    inventory_id: Union[UUID, str]
    raw_id: Union[UUID, str]
    quantity: Optional[int]


# Properties to receive via API on creation
class InventoryRecordCreate(InventoryRecordBase):
    pass


class InventoryRecordUpdate(InventoryRecordBase):
    id: str


# Properties to receive via API on update
class InventoryRecordInDBBase(InventoryRecordBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class InventoryRecord(InventoryRecordInDBBase):
    pass
