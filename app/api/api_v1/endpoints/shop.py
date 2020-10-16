from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import models
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=schemas.Shop)
def read_shop(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user shop.
    """
    shop = crud.shop.get(db=db, id=current_user.shop_id)
    return shop


@router.post("/", response_model=schemas.Shop)
def create_shop(
        *,
        db: Session = Depends(deps.get_db),
        shop_in: schemas.ShopCreate,
        current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Create new shop.
    """
    shop = crud.shop.create_with_owner(db, obj_in=shop_in, owner=current_user)
    return shop


@router.put("/{shop_id}", response_model=schemas.Shop)
def update_shop(
    *,
    db: Session = Depends(deps.get_db),
    shop_id: str,
    shop_in: schemas.ShopUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update a shop.
    """
    shop = crud.shop.get(db, id=shop_id)
    if not shop:
        raise HTTPException(
            status_code=404,
            detail="The shop with this id does not exist in the system",
        )
    shop = crud.shop.update(db, db_obj=shop, obj_in=shop_in)
    return shop
