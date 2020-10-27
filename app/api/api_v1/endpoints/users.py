import os
import traceback
from typing import Any, List, Dict, Optional, Union

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.utils import save_upload_file
from app import crud, schemas
from app.models import models
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from uuid import uuid4


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.User]]])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    take: int = 100,
    filter: str = None
) -> Any:
    """
    Retrieve users.
    """
    data = crud.user.get_multi(db, shop_id=str(current_user.shop_id), skip=skip, take=take, filter=filter)
    return data


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    avatar: Optional[bytes] = None,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_phone(db=db, phone=user_in.phone)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone number already exists in the system.",
        )
    if avatar is not None:
        avatar = File(avatar)
        try:
            file_id = uuid4()
            save_upload_file(avatar, f'app/static/avatars/{str(file_id)}.png')
            file_in = schemas.FileCreate(id=avatar.id, path=avatar.path)
            crud.file.create(db=db, obj_in=file_in)
            user_in.avatar = file_in
        except Exception:
            raise HTTPException(status_code=500, detail="Can't save photo")
    user = crud.user.create(db, obj_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: schemas.UserUpdate,
    avatar: Optional[bytes] = None,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if avatar is not None:
        avatar = File(avatar)
        if user_in.avatar.id:
            try:
                os.remove(user_in.avatar.path)
                save_upload_file(avatar, f'app/static/avatars/{user_in.avatar.id}.png')
                user_in.avatar.path = f'app/static/avatars/{user_in.avatar.id}.png'
                old_avatar = crud.file.get(db=db, id=user_in.avatar.id)
                avatar = crud.file.update(db=db, db_obj=old_avatar, obj_in=user_in.avatar.path)
            except Exception:
                traceback.format_exc()
                raise HTTPException(status_code=500, detail="Can't save photo")
        else:
            try:
                file_id = uuid4()
                save_upload_file(avatar, f'app/static/avatars/{str(file_id)}.png')
                avatar = crud.file.create(id=file_id, path=f'app/static/avatars/{str(file_id)}.png')
                file_in = schemas.FileCreate(id=avatar.id, path=avatar.path)
                user_in.avatar = file_in
            except Exception:
                raise HTTPException(status_code=500, detail="Can't save photo")
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.post("/init_superuser")
def create_super_user(db: Session = Depends(deps.get_db)) -> Any:
    """
    Create super user.
    """
    user = crud.user.get_by_phone(db, phone=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.SuperUserCreate(
            phone=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True
        )
        crud.user.create(db, obj_in=user_in)
        return 'ok'
    else:
        raise HTTPException(
            status_code=400,
            detail="Super user already exists in the system.",
        )


@router.post("/create_admin")
def create_admin(
        user_in: schemas.AdminCreate,
        db: Session = Depends(deps.get_db)) -> Any:
    """
    Create admin.
    """
    user = crud.user.get_by_phone(db=db, phone=user_in.phone)
    if not user:
        user = crud.user.create(db, obj_in=user_in)
        return 'ok'
    else:
        raise HTTPException(
            status_code=400,
            detail="Super user already exists in the system.",
        )
