from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone
from .invoice_record import InvoiceRecord, InvoiceRecordCreate


# Shared properties
class InvoiceBase(BaseModel):
    shop_id: Union[UUID, str]
    number: str
    date: datetime = datetime.utcnow()
    supplier: Optional[str]
    remark: Optional[str]
    payment_method: Optional[str] = "Наличные"

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


# Properties to receive via API on creation
class InvoiceCreate(InvoiceBase):
    records: Optional[List[InvoiceRecordCreate]] = []


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


class InvoicesResponse(BaseModel):
    totalCount: int
    data: List[Invoice]
