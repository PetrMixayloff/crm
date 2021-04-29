from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .raw import Raw


# Shared properties
class InvoiceRecordBase(BaseModel):
    raw_id: str
    price: Optional[float] = 0
    quantity: Optional[float] = 0


# Properties to receive via API on creation
class InvoiceRecordCreate(InvoiceRecordBase):
    pass


class InvoiceRecordUpdate(InvoiceRecordBase):
    id: str


# Properties to receive via API on update
class InvoiceRecordInDBBase(InvoiceRecordBase):
    id: UUID
    shop_id: UUID
    invoice_id: UUID
    raw_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class InvoiceRecord(InvoiceRecordInDBBase):
    pass
