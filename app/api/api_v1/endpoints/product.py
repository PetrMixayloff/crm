from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Product]]])
def read_product_by_shop_id(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user)
                            ) -> Any:
    """
    Get current product by shop id.
    """
    shop_id = str(current_user.shop_id)
    product = crud.product.get_multi(db, shop_id=shop_id)
    return product


@router.get("/{category_id}", response_model=Dict[str, Union[int, List[schemas.Product]]])
def read_product_by_category_id(*, db: Session = Depends(deps.get_db),
                                current_user: models.User = Depends(deps.get_current_active_user),
                                category_id: str) -> Any:
    """
    Get current product by category id.
    """
    product = crud.product.get_multi_by_category_id(db, category_id=category_id)
    return product


@router.get("/{product_id}", response_model=schemas.Product)
def read_product_by_id(*,
                       db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       product_id: str) -> Any:
    """
    Get current product by id.
    """
    product = crud.product.get(db, id=product_id)
    return product


@router.post("/", response_model=schemas.Product)
def create_product(*,
                   db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_add: schemas.ProductCreate,
                   raws: List[schemas.ProductRawRelationCreate]
                   ) -> Any:
    """
    Create new product.
    """
    product = crud.product.create_product(db, obj_in=product_add, raws=raws)
    return product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_update_in: schemas.ProductUpdate) -> Any:
    """
    Update product.
    """
    product = crud.product.get(db, id=product_update_in.id)
    product = crud.product.update(db, obj_in=product_update_in, db_obj=product)
    return product


@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_id: str) -> Any:
    """
    Delete product
    """
    product = crud.product.remove(db, id=product_id)
    return product
