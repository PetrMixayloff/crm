from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from .invoice_record import InvoiceRecord


# Shared properties
class InvoiceBase(BaseModel):
    shop_id: Union[UUID, str]
    number: str
    date: datetime = datetime.utcnow()
    supplier: Optional[str]
    remark: Optional[str]
    payment_method: Optional[str] = "Наличные"


# Properties to receive via API on creation
class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    id: str


# Properties to receive via API on update
class InvoiceInDBBase(InvoiceBase):
    id: UUID
    records: Optional[List[InvoiceRecord]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class Invoice(InvoiceInDBBase):
    pass
