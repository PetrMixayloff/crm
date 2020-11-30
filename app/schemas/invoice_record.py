from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class InvoiceRecordBase(BaseModel):
    shop_id: Union[UUID, str]
    invoice_id: Union[UUID, str]
    category_id: Union[UUID, str]
    raw_id: Union[UUID, str]
    price: Optional[float] = 0
    quantity: Optional[float] = 0
    total: Optional[float] = 0


# Properties to receive via API on creation
class InvoiceRecordCreate(InvoiceRecordBase):
    pass


class InvoiceRecordUpdate(InvoiceRecordBase):
    id: str


# Properties to receive via API on update
class InvoiceRecordInDBBase(InvoiceRecordBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class InvoiceRecord(InvoiceRecordInDBBase):
    pass