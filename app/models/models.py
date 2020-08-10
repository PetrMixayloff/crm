import datetime
from app.db.base_class import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    full_name = Column(String(255))
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=True)
    remark = Column(String)


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    token = Column(String, unique=True, index=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False