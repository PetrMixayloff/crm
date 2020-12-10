from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=schemas.RawUsageStandards)
def read_raw_usage_standards_by_id(*, db: Session = Depends(deps.get_db),
                                   raw_usage_standards_id: str,
                                   current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get raw_usage_standards by shop id.
    """
    raw_usage_standards = crud.raw_usage_standards.get(db, id=raw_usage_standards_id)
    return raw_usage_standards


@router.post("/", response_model=schemas.RawUsageStandards)
def create_raw_usage_standards(*, db: Session = Depends(deps.get_db),
                               current_user: models.User = Depends(deps.get_current_active_user),
                               obj_in: schemas.RawUsageStandardsCreate
                               ) -> Any:
    """
    Create raw usage standards.
    """
    raw_usage_standards = crud.raw_usage_standards.create(db, obj_in=obj_in)
    return raw_usage_standards


@router.put("/{id}", response_model=schemas.RawUsageStandards)
def update_raw_usage_standards_by_id(*, db: Session = Depends(deps.get_db),
                                     current_user: models.User = Depends(deps.get_current_active_user),
                                     obj_in: schemas.RawUsageStandardsUpdate,
                                     ) -> Any:
    """
    Update raw usage standards by raw_id.
    """
    in_base = crud.raw_usage_standards.get(db, id=obj_in.id)
    raw_usage_standards = crud.raw_usage_standards.update(db, db_obj=in_base, obj_in=obj_in)
    return raw_usage_standards


@router.delete("/{id}", response_model=schemas.RawUsageStandards)
def delete_raw_usage_standards(*, db: Session = Depends(deps.get_db),
                               current_user: models.User = Depends(deps.get_current_active_user),
                               raw_usage_standards_id: str) -> Any:
    """
    Delete raw usage standards
    """
    raw_usage_standards = crud.raw_usage_standards.remove(db, id=raw_usage_standards_id)
    return raw_usage_standards