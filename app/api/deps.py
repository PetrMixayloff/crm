from datetime import datetime
from enum import Enum
from typing import Generator, Callable, List, Tuple, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models import models
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

import copy
from app.db.session import inspector

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


class PermissionsEnum(Enum):
    read = 'read'
    edit = 'edit'


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        datetime_now = datetime.utcnow()
        setattr(user, 'last_login', datetime_now)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def check_permissions(key: str, value: Optional[PermissionsEnum.value]) -> Callable:

    async def user_has_permission(user: models.User = Depends(get_current_user)) -> models.User:
        if user.is_superuser or not user.is_staff or value is None:
            return user
        code_lookup = ('read', 'edit')
        if code_lookup.index(value) > code_lookup.index(user.permissions[key]):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return user_has_permission


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if crud.user.is_staff(current_user) or crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_all_schemas_models():
    schemas_models = dict()

    schemas = inspector.get_schema_names()

    for schema in schemas:
        tables = inspector.get_table_names(schema)
        for tab in tables:
            mapped_columns = [mapping_column(c) for c in inspector.get_columns(tab, schema)]

            schemas_models['{}.{}'.format(schema, tab)] = mapped_columns

    return schemas_models


def mapping_column(col):
    mapped = copy.copy(col)
    mapped['type'] = mapping_types(type(col['type']).__name__)
    del mapped['default']
    del mapped['autoincrement']
    return mapped


def mapping_types(type_str):
    res = ''
    if type_str.find('VARCHAR') != -1:
        res = 'string'
    elif type_str.find('TEXT') != -1:
        res = 'string'
    elif type_str.find('INTEGER') != -1:
        res = 'number'
    elif type_str.find('TIMESTAMP') != -1:
        res = 'date'
    elif type_str.find('BOOLEAN') != -1:
        res = 'boolean'
    elif type_str.find('ENUM') != -1:
        res = 'string'
    elif type_str.find('JSON') != -1:
        res = 'string'
    else:
        print(type_str)
    return res
