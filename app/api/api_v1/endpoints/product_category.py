from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, List, Dict, Union
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.ProductCategory]]])
def read_product_categories(db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user)
                            ) -> Any:
    """
    Get product categories for current user.
    """
    shop_id = str(current_user.shop_id)
    product_category = crud.product_category.get_multi(db, shop_id=shop_id)
    return product_category


@router.post("/", response_model=schemas.ProductCategory)
def create_product_category(*, db: Session = Depends(deps.get_db),
                            product_category_add: schemas.ProductCategoryCreate
                            ) -> Any:
    """
    Create new create product category.
    """
    product_category = crud.product_category.create_product_category(db, obj_in=product_category_add)
    return product_category


@router.put("/update_product_category", response_model=schemas.ProductCategory)
def update_product_category(*, db: Session = Depends(deps.get_db),
                            product_category_in: schemas.ProductCategoryUpdate
                            ) -> Any:
    """
    Update product category.
    """
    product_category = crud.product_category.update_product_category(db, obj_in=product_category_in)
    return product_category


@router.get("/{category_id}", response_model=Dict[str, Union[int, List[schemas.ProductCategory]]])
def read_product_category_by_id(db: Session = Depends(deps.get_db),
                                category_id: str = None,
                                skip: int = 0,
                                take: int = 100,
                                filter: str = None
                                ) -> Any:
    """
    Get current product by category_id.
    """
    product_category = crud.product_category.get_multi_product_category_by_id(
        db,
        category_id=category_id,
        skip=skip, take=take, filter=filter
    )
    return product_category


@router.delete("/{category_id}", response_model=schemas.ProductCategory)
def delete_product_category_by_id(db: Session = Depends(deps.get_db),
                                  category_id: str = None,
                                  ) -> Any:
    """
    Delete product by category_id.
    """
    product_category = crud.product_category.remove(db, id=category_id)
    return product_category



