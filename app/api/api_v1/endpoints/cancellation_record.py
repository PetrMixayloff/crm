from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Cancellation]]])
def read_cancellation_record_by_shop_id(*, db: Session = Depends(deps.get_db),
                                        current_user: models.User = Depends(deps.get_current_active_user),
                                        skip: int = 0,
                                        take: int = 100,
                                        filter: str = None
                                        ) -> Any:
    """
    Get cancellation record by shop id.
    """
    shop_id = str(current_user.shop_id)
    cancellation_record = crud.cancellation.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return cancellation_record


@router.post("/", response_model=schemas.Cancellation)
def create_cancellation_record(*, db: Session = Depends(deps.get_db),
                               current_user: models.User = Depends(deps.get_current_active_user),
                               cancellation_in: schemas.CancellationCreate) -> Any:
    """
    Create new cancellation record.
    """
    cancellation = crud.cancellation.create(db, obj_in=cancellation_in)
    return cancellation
