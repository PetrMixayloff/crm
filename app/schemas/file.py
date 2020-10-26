from pydantic import BaseModel
from typing import Union, Optional
from uuid import UUID


# Shared properties
class FileBase(BaseModel):
    id: str
    product_id: Optional[Union[UUID, str]] = None
    user_id: Optional[Union[UUID, str]] = None
    path: str


# Properties to receive via API on creation
class FileCreate(FileBase):
    id: Union[UUID, str]


class FileUpdate(FileBase):
    id: str


# Properties to receive via API on update
class FileInDBBase(FileBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class File(FileInDBBase):
    pass
