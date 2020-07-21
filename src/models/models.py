import datetime
from . import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    login = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255))
    last_login = db.Column(db.DateTime, nullable=True)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=True)
    remark = db.Column(db.String)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    token = db.Column(db.String, unique=True, index=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False