from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.RawUsageStandards]]])
def read_standards_by_shop_id(*, db: Session = Depends(deps.get_db),
                              current_user: models.User = Depends(deps.get_current_active_user),
                              skip: int = 0,
                              take: int = 100,
                              filter: str = None) -> Any:
    """
    Get raw_usage_standards by shop_id.
    """
    shop_id = str(current_user.shop_id)
    standards = crud.raw_usage_standards.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return standards


@router.post("/", response_model=schemas.RawUsageStandards)
def create_standards(*, db: Session = Depends(deps.get_db),
                     current_user: models.User = Depends(deps.get_current_active_user),
                     obj_in: schemas.RawUsageStandardsCreate) -> Any:
    """
    Create raw usage standards.
    """
    standards = crud.raw_usage_standards.create(db, obj_in=obj_in)
    return standards


@router.put("/{id}", response_model=schemas.RawUsageStandards)
def update_standards_by_id(*, db: Session = Depends(deps.get_db),
                           current_user: models.User = Depends(deps.get_current_active_user),
                           obj_in: schemas.RawUsageStandardsUpdate) -> Any:
    """
    Update raw usage standards by raw_id.
    """
    in_base = crud.raw_usage_standards.get(db, id=obj_in.id)
    standards = crud.raw_usage_standards.update(db, db_obj=in_base, obj_in=obj_in)
    return standards


@router.delete("/{id}", response_model=schemas.RawUsageStandards)
def delete_standards(*, db: Session = Depends(deps.get_db),
                     current_user: models.User = Depends(deps.get_current_active_user),
                     standards_id: str) -> Any:
    """
    Delete raw usage standards
    """
    standards = crud.raw_usage_standards.remove(db, id=standards_id)
    return standards