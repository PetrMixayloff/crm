from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models import models
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email


router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Create new user.
    """
    shop_id = user_in.shop_id
    user = crud.user.check_user_login(db=db, login=user_in.login, shop_id=shop_id)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
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
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
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
    user = crud.user.get_by_login(db, login=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            login=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_staff=False
        )
        user = crud.user.create(db, obj_in=user_in)
        return 'ok'
    else:
        raise HTTPException(
            status_code=400,
            detail="Super user already exists in the system.",
        )


@router.post("/create_admin")
def create_admin(
        user_in: schemas.UserCreate,
        db: Session = Depends(deps.get_db)) -> Any:
    """
    Create admin.
    """
    user = crud.user.get_by_login(db, login=user_in.login)
    if not user:
        user = crud.user.create(db, obj_in=user_in)
        return 'ok'
    else:
        raise HTTPException(
            status_code=400,
            detail="Super user already exists in the system.",
        )
