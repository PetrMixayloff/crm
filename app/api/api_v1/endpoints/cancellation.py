from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=schemas.CancellationsResponse)
def read_cancellations(db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       skip: int = 0,
                       take: int = 100,
                       filter: str = None
                       ) -> schemas.CancellationsResponse:
    """
    Получение списка расходных накладных для магазина.
    """
    shop_id = str(current_user.shop_id)
    cancellation = crud.cancellation.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return cancellation


@router.get("/{cancellation_id}", response_model=schemas.Cancellation)
def read_cancellation_by_id(cancellation_id: str,
                            db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            ) -> schemas.Cancellation:
    """
    Получение расходной накладной по id.
    """
    cancellation = crud.cancellation.get(db, id=cancellation_id)
    return cancellation


@router.post("/", response_model=schemas.Cancellation)
def create_cancellation(cancellation_in: schemas.CancellationCreate,
                        db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user),
                        ) -> schemas.Cancellation:
    """
    Создание новой расходной накладной.
    """
    cancellation = crud.cancellation.create_cancellation(db, obj_in=cancellation_in)
    return cancellation
