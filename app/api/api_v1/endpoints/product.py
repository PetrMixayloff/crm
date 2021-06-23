from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List, Optional
from app.api import deps
from app.models import models
from app.models.models import ProductRawRelation

router = APIRouter()


@router.get("/", response_model=schemas.ProductResponse)
def read_products(*, db: Session = Depends(deps.get_db),
                  current_user: models.User = Depends(deps.get_current_active_user),
                  skip: int = 0,
                  take: int = 100,
                  filter: str = None
                  ) -> Any:
    """
    Get products by shop id.
    """
    shop_id = str(current_user.shop_id)
    product = crud.product.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return product


@router.get("/by_category/{category_id}", response_model=schemas.ProductResponse)
def read_product_by_category_id(*, db: Session = Depends(deps.get_db),
                                current_user: models.User = Depends(deps.get_current_active_user),
                                category_id: str) -> Any:
    """
    Get current product by category id.
    """
    filter_options = ['category_id', '=', category_id]
    product = crud.product.get_multi(db, filter=filter_options)
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


@router.post("/", response_model=Union[schemas.Product, schemas.ProductSet])
def create_product(*,
                   db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_in: Union[schemas.ProductCreate, schemas.ProductSetCreate]
                   ) -> Any:
    """
    Create new product.
    """
    product = crud.product.create_product(db, obj_in=product_in)
    return product


@router.put("/{product_id}", status_code=204)
def update_product(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_update_in: schemas.ProductUpdate
                   ) -> Any:
    """
    Update product.
    """
    product = crud.product.get(db, id=product_update_in.id)
    crud.product.update_product(db, obj_in=product_update_in, db_obj=product)


@router.delete("/{product_id}", status_code=204)
def delete_product(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   product_id: str) -> Any:
    """
    Delete product
    """
    crud.product.disable(db, id=product_id)


@router.delete("/raw_relation/{raw_id}", status_code=204)
def delete_raw_nested_with_product(*, db: Session = Depends(deps.get_db),
                                   current_user: models.User = Depends(deps.get_current_active_user),
                                   raw_id: str) -> Any:
    """
    Delete nested raw
    """
    crud.product_raw_relation.remove(db=db, id=raw_id)
