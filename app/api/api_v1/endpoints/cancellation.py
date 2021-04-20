from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Cancellation]]])
def read_cancellation_by_shop_id(*, db: Session = Depends(deps.get_db),
                                 current_user: models.User = Depends(deps.get_current_active_user),
                                 skip: int = 0,
                                 take: int = 100,
                                 filter: str = None
                                 ) -> Any:
    """
    Get Cancellation by shop id.
    """
    shop_id = str(current_user.shop_id)
    cancellation = crud.cancellation.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return cancellation


@router.get("/{cancellation_id}", response_model=schemas.Cancellation)
def read_cancellation_by_id(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            cancellation_id: str) -> Any:
    """
    Get current cancellation by id.
    """
    cancellation = crud.cancellation.get(db, id=cancellation_id)
    return cancellation


@router.post("/", response_model=schemas.Cancellation)
def create_cancellation(*, db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user),
                        cancellation_in: schemas.CancellationCreate) -> Any:
    """
    Create new cancellation.
    """
    cancellation = crud.cancellation.create_cancellation(db, obj_in=cancellation_in)
    return cancellation


@router.delete("/{cancellation_id}", response_model=schemas.Cancellation)
def delete_cancellation(*, db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user),
                        cancellation_id: str) -> Any:
    """
    Delete cancellation.
    """
    cancellation = crud.cancellation.remove(db, id=cancellation_id)
    return cancellation
