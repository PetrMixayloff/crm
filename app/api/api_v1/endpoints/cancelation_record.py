from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.CancelationRecord]]])
def read_cancelation_record_by_shop_id(*, db: Session = Depends(deps.get_db),
                                       current_user: models.User = Depends(deps.get_current_active_user),
                                       skip: int = 0,
                                       take: int = 100,
                                       filter: str = None
                                       ) -> Any:
    """
    Get cancelation record by shop id.
    """
    shop_id = str(current_user.shop_id)
    cancelation_record = crud.cancelation_record.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return cancelation_record


@router.post("/", response_model=schemas.CancelationRecord)
def create_cancelation_record(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            cancelation_in: schemas.CancelationRecordCreate,
                            raw_remains_update: List[schemas.RawRemainsDetailUpdate]) -> Any:
    """
    Create new cancelation record.
    """
    cancelation_record = crud.cancelation_record.create_cancelation_record(db, obj_in=cancelation_in,
                                                                         raw_remains_update=raw_remains_update
                                                                         )
    return cancelation_record
