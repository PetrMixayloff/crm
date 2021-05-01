from pydantic import BaseModel
from uuid import UUID


# Shared properties
class CancellationRecordBase(BaseModel):
    raw_id: str
    raw_remains_details_id: str
    quantity: float
    price: float


# Properties to receive via API on creation
class CancellationRecordCreate(CancellationRecordBase):
    pass


# Properties to receive via API on update
class CancellationRecordInDBBase(CancellationRecordBase):
    id: UUID
    cancellation_id: UUID
    raw_remains_details_id: UUID
    raw_id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class CancellationRecord(CancellationRecordInDBBase):
    pass
