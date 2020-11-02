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
def create_product_category(product_category_add: schemas.ProductCategoryCreate,
                            current_user: models.User = Depends(deps.get_current_active_user),
                            db: Session = Depends(deps.get_db)
                            ) -> Any:
    """
    Create new create product category.
    """
    product_category = crud.product_category.create(db, obj_in=product_category_add)
    return product_category


@router.put("/{category_id}", response_model=schemas.ProductCategory)
def update_product_category(category_id: str,
                            product_category_in: schemas.ProductCategoryUpdate,
                            db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user)
                            ) -> Any:
    """
    Update product category.
    """
    category_obj = crud.product_category.get(db, id=category_id)
    product_category = crud.product_category.update(db, db_obj=category_obj, obj_in=product_category_in)
    return product_category


@router.get("/{category_id}", response_model=schemas.ProductCategory)
def read_product_category_by_id(category_id: str,
                                db: Session = Depends(deps.get_db),
                                current_user: models.User = Depends(deps.get_current_active_user)
                                ) -> Any:
    """
    Get product category by id.
    """
    product_category = crud.product_category.get(db, category_id=category_id)
    return product_category


@router.delete("/{category_id}", response_model=schemas.ProductCategory)
def delete_product_category_by_id(db: Session = Depends(deps.get_db),
                                  category_id: str = None,
                                  ) -> Any:
    """
    Delete product category by id.
    """
    product_category = crud.product_category.remove(db, id=category_id)
    return product_category
