from typing import Optional, List, Union
from pydantic import BaseModel
from uuid import UUID
from .raw import Raw


# Shared properties
class RawCategoryBase(BaseModel):
    name: str
    parent_id: Optional[Union[str, UUID]] = None
    shop_id: Union[str, UUID]
    description: Optional[str] = None


# Properties to receive via API on creation
class RawCategoryCreate(RawCategoryBase):
    pass


class RawCategoryUpdate(RawCategoryBase):
    pass


# Properties to receive via API on update
class RawCategoryInDBBase(RawCategoryBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class RawCategoryInDB(RawCategoryInDBBase):
    subcategories: Optional[List[RawCategoryInDBBase]] = []


class RawCategory(RawCategoryInDB):
    subcategories: Optional[List[RawCategoryInDB]] = []
