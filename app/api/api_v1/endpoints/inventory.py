from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=schemas.InventoriesResponse)
def read_inventory_by_shop_id(*, db: Session = Depends(deps.get_db),
                              current_user: models.User = Depends(deps.get_current_active_user),
                              skip: int = 0,
                              take: int = 100,
                              filter: str = None
                              ) -> Any:
    """
    Get inventory by shop id.
    """
    shop_id = str(current_user.shop_id)
    inventories = crud.inventory.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return inventories


@router.post("/", response_model=schemas.Inventory)
def create_inventory(*, db: Session = Depends(deps.get_db),
                     current_user: models.User = Depends(deps.get_current_active_user),
                     inventory_in: schemas.InventoryCreate) -> Any:
    """
    Create new inventory.
    """
    inventory_in.user_id = str(current_user.id)
    inventory = crud.inventory.create_inventory(db, obj_in=inventory_in)
    return inventory
