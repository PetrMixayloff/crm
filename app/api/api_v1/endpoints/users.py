from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.models import models
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=schemas.UsersResponse)
async def read_users(
        async_db: AsyncSession = Depends(deps.get_async_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        skip: int = 0,
        take: int = 100,
        sort: str = None,
        filter: str = None
):
    """
    Retrieve users.
    """
    data = await crud.user.get_multi_async(async_db=async_db, shop_id=str(current_user.shop_id),
                                           skip=skip, take=take, sort=sort, filter=filter)
    return data


@router.post("/", response_model=schemas.User)
async def create_user(user_in: schemas.UserCreate, async_db: AsyncSession = Depends(deps.get_async_db),
                      current_user: models.User = Depends(deps.get_current_active_admin_user)):
    """
    Create new user.
    """
    user = await crud.user.get_by_phone_async(async_db=async_db, phone=user_in.phone)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone number already exists in the system.",
        )
    user = await crud.user.create_async(async_db=async_db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: str,
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
):
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    return user


@router.put("/{user_id}", status_code=204)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> None:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    crud.user.update(db, db_obj=user, obj_in=user_in)


@router.post("/init_superuser", status_code=204)
def create_super_user(db: Session = Depends(deps.get_db)) -> None:
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
        return
    else:
        raise HTTPException(
            status_code=409,
            detail="Super user already exists in the system.",
        )


@router.post("/create_admin")
def create_admin(
        user_in: schemas.AdminCreate,
        db: Session = Depends(deps.get_db)):
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


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str,
                db: Session = Depends(deps.get_db),
                current_user: models.User = Depends(deps.get_current_active_admin_user)
                ) -> None:
    """
    Delete user.
    """
    user = crud.user.remove(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
