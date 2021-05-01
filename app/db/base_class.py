from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, DateTime


@as_declarative()
class Base:
    __name__: str

    # Generate __table_name__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        table_name = ''
        for letter in cls.__name__:
            table_name += f'_{letter.lower()}' if letter.isupper() else letter
        return table_name[1:]

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    is_active = Column(Boolean, nullable=False, default=True)
