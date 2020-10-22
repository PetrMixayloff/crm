from typing import List
from uuid import UUID
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.crud.base import CRUDBase
from app.models import models
from app.models.models import ProductCategory
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):
    def create_product_category(self, db: Session,
                                obj_in: ProductCategoryCreate,
                                current_user: models.User = Depends(deps.get_current_active_admin_user),
                                ) -> ProductCategory:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_product(
            self, db: Session, category_id: UUID) -> ProductCategory:
        return db.query(self.model).filter(ProductCategory.category_id == category_id).all()

    def update_product_category(self, db: Session, *,
                                obj_in: ProductCategoryUpdate,
                                ) -> ProductCategory:
        db_obj = crud.product_category.get(db, id=obj_in.id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product_category = CRUDProductCategory(ProductCategory)
