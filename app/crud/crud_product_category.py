from typing import Dict, Union, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud
from app.crud.base import CRUDBase
from app.models.models import ProductCategory, User
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):
    def create_product_category(self, db: Session,
                                obj_in: ProductCategoryCreate,
                                ) -> ProductCategory:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_product_category(self, db: Session, *,
                                obj_in: ProductCategoryUpdate) -> ProductCategory:
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

    def get_multi_product_category(
            self, db: Session, shop_id: str, skip: int = 0, take: int = 100, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        product_category = db.query(self.model).filter(self.model.shop_id == shop_id)
        if filter is not None:
            product_category = self.filter_query(product_category, filter)
        product_category = product_category.offset(skip).limit(take).all()
        data = {
            'totalCount': len(product_category),
            'data': product_category
        }
        return data

    def get_multi_product_category_by_id(
            self, db: Session, category_id: str, skip: int = 0, take: int = 100, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        product_category_by_id = db.query(self.model).filter(self.model.id == category_id)
        if filter is not None:
            product_category_by_id = self.filter_query(product_category_by_id, filter)
        product_category_by_id = product_category_by_id.offset(skip).limit(take).all()
        data = {
            'totalCount': len(product_category_by_id),
            'data': product_category_by_id
        }
        return data


product_category = CRUDProductCategory(ProductCategory)
