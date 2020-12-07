from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, List, Dict, Union
from app.api import deps
from app.models import models

router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.RawCategory]]])
def read_raw_categories(db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user)
                        ) -> Any:
    """
    Get raw categories for current user.
    """
    shop_id = str(current_user.shop_id)
    raw_category = crud.raw_category.get_multi(db, shop_id=shop_id)
    return raw_category


@router.post("/", response_model=schemas.RawCategory)
def create_raw_category(raw_category_in: schemas.RawCategoryCreate,
                        current_user: models.User = Depends(deps.get_current_active_user),
                        db: Session = Depends(deps.get_db)
                        ) -> Any:
    """
    Create raw category.
    """
    raw_category = crud.raw_category.create(db, obj_in=raw_category_in)
    return raw_category


@router.put("/{category_id}", response_model=schemas.RawCategory)
def update_raw_category(category_id: str,
                        raw_category_in: schemas.RawCategoryUpdate,
                        db: Session = Depends(deps.get_db),
                        current_user: models.User = Depends(deps.get_current_active_user)
                        ) -> Any:
    """
    Update raw category.
    """
    category_obj = crud.raw_category.get(db, id=category_id)
    raw_category = crud.raw_category.update(db, db_obj=category_obj, obj_in=raw_category_in)
    return raw_category


@router.get("/{category_id}", response_model=schemas.RawCategory)
def read_raw_category_by_id(category_id: str,
                            db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user)
                            ) -> Any:
    """
    Get raw category by id.
    """
    raw_category = crud.raw_category.get(db, id=category_id)
    return raw_category


@router.delete("/{category_id}", response_model=List[schemas.RawCategory])
def delete_raw_category_by_id(db: Session = Depends(deps.get_db),
                              category_id: str = None,
                              ) -> Any:
    """
    Delete raw category and all subcategories by id.
    """
    raw_categories = crud.raw_category.recursive_disable(db, id=category_id)
    return raw_categories
