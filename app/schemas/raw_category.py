from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .raw import Raw


# Shared properties
class RawCategoryBase(BaseModel):
    name: str
    shop_id: Union[str, UUID]
    is_active: Optional[bool] = True
    description: Optional[str] = None


# Properties to receive via API on creation
class RawCategoryCreate(RawCategoryBase):
    pass


class RawCategoryUpdate(RawCategoryBase):
    pass


# Properties to receive via API on update
class RawCategoryInDBBase(RawCategoryBase):
    id: UUID
    raws: Optional[List[Raw]] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class RawCategory(RawCategoryInDBBase):
    pass
