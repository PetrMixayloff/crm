from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Cancelation]]])
def read_cancelation_by_shop_id(*, db: Session = Depends(deps.get_db),
                                current_user: models.User = Depends(deps.get_current_active_user),
                                skip: int = 0,
                                take: int = 100,
                                filter: str = None
                                ) -> Any:
    """
    Get Cancelation by shop id.
    """
    shop_id = str(current_user.shop_id)
    cancelation = crud.cancelation.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return cancelation


@router.get("/{cancelation_id}", response_model=schemas.Invoice)
def read_cancelation_by_id(*, db: Session = Depends(deps.get_db),
                           current_user: models.User = Depends(deps.get_current_active_user),
                           cancelation_id: str) -> Any:
    """
    Get current cancelation by id.
    """
    cancelation = crud.cancelation.get(db, id=cancelation_id)
    return cancelation


@router.post("/", response_model=schemas.Cancelation)
def create_cancelation(*, db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       cancelation_in: schemas.CancelationCreate) -> Any:
    """
    Create new cancelation.
    """
    cancelation = crud.cancelation.create_cancelation(db, obj_in=cancelation_in)
    return cancelation


@router.put("/{cancelation_id}", response_model=schemas.Cancelation)
def update_cancelation(*, db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       cancelation_record_update: List[schemas.CancelationRecordUpdate],
                       raw_remains_update: List[schemas.RawRemainsDetailUpdate],
                       cancelation_update_in: schemas.CancelationUpdate) -> Any:
    """
    Update cancelation.
    """
    cancelation = crud.cancelation.get(db, id=cancelation_update_in.id)
    cancelation = crud.cancelation.update_cancelation(db, obj_in=cancelation_update_in, db_obj=cancelation,
                                                      invoice_record_update=cancelation_record_update,
                                                      raw_remains_update=raw_remains_update)
    return cancelation


@router.delete("/{cancelation_id}", response_model=schemas.Invoice)
def delete_cancelation(*, db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       cancelation_id: str) -> Any:
    """
    Delete cancelation.
    """
    cancelation = crud.cancelation.remove(db, id=cancelation_id)
    return cancelation
