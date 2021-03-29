from app import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List, Optional
from app.api import deps
from app.models import models
from app.models.models import ProductRawRelation

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Order]]])
def read_orders(*, db: Session = Depends(deps.get_db),
                current_user: models.User = Depends(deps.get_current_active_user),
                skip: int = 0,
                take: int = 100,
                filter: str = None
                ) -> Any:
    """
    Get orders by shop id.
    """
    orders = crud.order.get_multi(db, shop_id=str(current_user.shop_id), skip=skip, take=take, filter=filter)
    return orders


@router.post("/", response_model=schemas.Order)
def create_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: schemas.OrderCreate,
        current_user: models.User = Depends(deps.get_current_active_admin_user)
) -> Any:
    """
    Create new order.
    """
    order_in.created_by_id = current_user.id
    order = crud.order.create(db=db, obj_in=order_in)
    return order


@router.get("/{order_id}", response_model=schemas.Order)
def get_order_by_id(
        order_id: str,
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific order by id.
    """
    order = crud.order.get(db, id=order_id)
    return order


@router.put("/{order_id}", response_model=schemas.Order)
def update_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: str,
        order_in: schemas.OrderUpdate,
        current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update an order.
    """
    order = crud.order.get(db, id=order_id)
    order = crud.order.update(db, db_obj=order, obj_in=order_in)
    return order


@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: str,
                 db: Session = Depends(deps.get_db),
                 current_user: models.User = Depends(deps.get_current_active_admin_user)
                 ) -> None:
    """
    Delete order.
    """
    order = crud.order.remove(db, id=order_id)
    return order
