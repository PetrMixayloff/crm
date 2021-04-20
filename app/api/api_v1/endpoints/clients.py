from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List, Optional
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Client]]])
def read_clients(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        skip: int = 0,
        take: int = 100,
        filter: str = None
) -> Any:
    """
    Get clients.
    """
    clients = crud.client.get_multi(db, shop_id=str(current_user.shop_id), skip=skip, take=take, filter=filter)
    return clients


@router.get("/{phone}", response_model=schemas.Client)
def read_client_by_phone(
        phone: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Optional[models.Client]:
    """
    Get client by phone number.
    """
    client = crud.client.get_by_phone(db, phone=phone)
    return client
