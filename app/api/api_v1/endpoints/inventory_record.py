from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.InventoryRecord]]])
def read_inventory_record_by_shop_id(*, db: Session = Depends(deps.get_db),
                                     current_user: models.User = Depends(deps.get_current_active_user),
                                     skip: int = 0,
                                     take: int = 100,
                                     filter: str = None
                                     ) -> Any:
    """
    Get inventory record by shop id.
    """
    shop_id = str(current_user.shop_id)
    inventory_record = crud.inventory_record.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return inventory_record


@router.post("/", response_model=schemas.InventoryRecord)
def create_inventory_record(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            inventory_in: schemas.InventoryRecordCreate,
                            raw_remains_update: List[schemas.RawRemainsDetailUpdate]) -> Any:
    """
    Create new inventory record.
    """
    inventory_record = crud.inventory_record.create_inventory_record(db, obj_in=inventory_in,
                                                                     raw_remains_update=raw_remains_update
                                                                     )
    return inventory_record
