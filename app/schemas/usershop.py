from pydantic import BaseModel
from uuid import UUID


# Shared properties
class UserShopBase(BaseModel):
    user_id: UUID
    shop_id: UUID
    position: str = None


# Properties to receive via API on creation
class UserShopCreate(UserShopBase):
    pass


# Properties to receive via API on update
class UserShopInDBBase(UserShopBase):
    id: UUID

    class Config:
        orm_mode = True


class UserShopUpdate(UserShopInDBBase):
    pass


# Additional properties to return via API
class UserShopRelation(UserShopInDBBase):
    pass
