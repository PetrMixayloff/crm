from app import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from app.api import deps

router = APIRouter()


@router.post("/create_product_category", response_model=schemas.ProductCategory)
def create_product_category(*, db: Session = Depends(deps.get_db),
                            product_category_add: schemas.ProductCategoryCreate
                            ) -> Any:
    """
    Create new create product category.
    """
    product_category = crud.product_category.create(db, obj_in=product_category_add)
    return product_category


@router.put("/update_product_category", response_model=schemas.ProductCategory)
def update_product_category(*, db: Session = Depends(deps.get_db),
                            product_category_add: schemas.ProductCategoryUpdate,
                            ) -> Any:
    """
    Update product category.
    """
    product_category = crud.product_category.update_product_category(db, obj_in=product_category_add)
    return product_category


@router.get("/", response_model=List[schemas.ProductCategory])
def read_product(db: Session = Depends(deps.get_db)) -> Any:
    """
    Get current product.
    """
    return crud.product_category.get_multi(db)
