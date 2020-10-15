from app import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_product(
        db: Session = Depends(deps.get_db)

) -> Any:
    """
    Get current product.
    """
    return crud.product.get_multi(db)


@router.get("/{product_id}", response_model=List[schemas.Product])
def read_product_by_id(
        product_id: str,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get current product by id.
    """
    product = crud.product.get(db, id=product_id)
    return product


@router.post("/create_product", response_model=List[schemas.Product])
def create_product(*,
                   db: Session = Depends(deps.get_db),
                   product_add: schemas.ProductCreate)\
        -> Any:
    """
    Create new product.
    """
    product = crud.product.create(db, obj_in=product_add)
    return product


@router.put("/{product_id}", response_model=List[schemas.ProductUpdate])
def update_product_by_id(
        *,
        db: Session = Depends(deps.get_db),
        product_id: str,
        product_update: schemas.ProductUpdate,

) -> Any:
    """
    Update product.
    """
    product = crud.product.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="The product with this id does not exist in the system",
        )
    product = crud.product.update(db, db_obj=product, obj_in=product_update)
    return product


@router.delete("/{product_id}", response_model=List[schemas.Product])
def delete_product(
        *,
        db: Session = Depends(deps.get_db),
        product_id: str,

) -> Any:
    """
    Delete product.
    """
    product = crud.product.get(db, id=product_id)
    product = crud.product.remove(db, db_obj=product)
    return 'done!'
