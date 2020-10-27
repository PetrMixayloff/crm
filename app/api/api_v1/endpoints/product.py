from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Product]]])
def read_product(db: Session = Depends(deps.get_db),
                 current_user: models.User = Depends(deps.get_current_active_user),
                 category_id: str = None,
                 skip: int = 0,
                 take: int = 100,
                 filter: str = None
                 ) -> Any:
    """
    Get current product.
    """
    shop_id = current_user.shop_id
    product = crud.product.get_multi_product(db, shop_id=shop_id,
                                             category_id=category_id,
                                             skip=skip, take=take, filter=filter)
    return product


@router.get("/{product_id}", response_model=Dict[str, Union[int, List[schemas.Product]]])
def read_product_by_id(*,
                       db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       category_id: str = None,
                       product_id: str = None,
                       skip: int = 0,
                       take: int = 100,
                       filter: str = None) -> Any:
    """
    Get current product by id.
    """
    shop_id = current_user.shop_id
    product = crud.product.get_multi_product_by_id(db, shop_id=shop_id,
                                                   category_id=category_id,
                                                   product_id=product_id,
                                                   skip=skip, take=take, filter=filter)
    return product


@router.post("/create_product", response_model=schemas.Product)
def create_product(*,
                   db: Session = Depends(deps.get_db),
                   product_add: schemas.ProductCreate,
                   ) -> Any:
    """
    Create new product.
    """
    product = crud.product.create(db, obj_in=product_add)
    return product


@router.put("/update_product", response_model=schemas.Product)
def update_product(*, db: Session = Depends(deps.get_db),
                   product_update_in: schemas.ProductUpdate) -> Any:
    """
    Update product.
    """
    product = crud.product.update_product(db, obj_in=product_update_in)
    return product


@router.delete("/delete_product", response_model=schemas.Product)
def delete_product(db: Session = Depends(deps.get_db),
                   product_id: str = None,
                   ) -> Any:
    """
    Delete product
    """
    product = crud.product.remove(db, id=product_id)
    return product