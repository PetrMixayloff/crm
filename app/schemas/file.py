from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID


# Shared properties
class FileBase(BaseModel):
    path: str


# Properties to receive via API on creation
class FileCreate(FileBase):
    pass


# Properties to receive via API on update
class FileInDBBase(FileBase):
    id: UUID

    class Config:
        orm_mode = True


class FileUpdate(FileInDBBase):
    pass


# Additional properties to return via API
class File(FileInDBBase):
    pass
