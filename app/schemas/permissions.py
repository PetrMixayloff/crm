from typing import Optional
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class PermissionsBase(BaseModel):
    user_id: UUID
    orders: Optional[str] = None
    products: Optional[str] = None
    raw: Optional[str] = None
    clients: Optional[str] = None
    staff: Optional[str] = None
    warehouse: Optional[str] = None


# Properties to receive via API on creation
class PermissionsCreate(PermissionsBase):
    pass


class PermissionsUpdate(PermissionsBase):
    pass


# Properties to receive via API on update
class PermissionsInDBBase(PermissionsBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permissions(PermissionsInDBBase):
    pass
