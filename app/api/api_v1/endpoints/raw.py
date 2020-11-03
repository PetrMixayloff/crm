from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Raw]]])
def read_raw_by_shop_id(*, db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user)
                        ) -> Any:
    """
    Get current raw by shop id.
    """
    shop_id = str(current_user.shop_id)
    raw = crud.raw.get_multi(db, shop_id=shop_id)
    return raw


@router.get("/{category_id}", response_model=Dict[str, Union[int, List[schemas.Raw]]])
def read_raw_by_category_id(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            category_id: str) -> Any:
    """
    Get current raw by category id.
    """
    raw = crud.product.get_multi_by_category_id(db, category_id=category_id)
    return raw


@router.get("/{raw_id}", response_model=schemas.Raw)
def read_raw_by_id(*,
                   db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   raw_id: str) -> Any:
    """
    Get current raw by id.
    """
    raw = crud.raw.get(db, id=raw_id)
    return raw


@router.post("/create", response_model=schemas.Raw)
def create_raw(*,
               db: Session = Depends(deps.get_db),
               current_user: models.User = Depends(deps.get_current_active_user),
               raw_in: schemas.RawCreate,
               ) -> Any:
    """
    Create new raw.
    """
    raw = crud.raw.create(db, obj_in=raw_in)
    return raw


@router.put("/update{raw_id}", response_model=schemas.Raw)
def update_raw(*, db: Session = Depends(deps.get_db),
               current_user: models.User = Depends(deps.get_current_active_user),
               raw_update_in: schemas.RawUpdate) -> Any:
    """
    Update raw.
    """
    raw = crud.raw.get(db, id=raw_update_in.id)
    raw = crud.raw.update(db, obj_in=raw_update_in, db_obj=raw)
    return raw


@router.delete("/delete{raw_id}", response_model=schemas.Raw)
def delete_raw(*, db: Session = Depends(deps.get_db),
               current_user: models.User = Depends(deps.get_current_active_user),
               raw_id: str) -> Any:
    """
    Delete raw
    """
    raw = crud.raw.remove(db, id=raw_id)
    return raw