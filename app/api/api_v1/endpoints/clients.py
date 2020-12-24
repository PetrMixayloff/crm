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


@router.get("/{client_id}", response_model=schemas.Client)
def read_client_by_id(
        db: Session = Depends(deps.get_db),
        client_id: str = None,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get client by id.
    """
    client = crud.client.get(db, id=client_id)
    return client
