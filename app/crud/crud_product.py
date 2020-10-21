from typing import List
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product, ProductCategory, Shop
from app.schemas import ProductCreate, ProductUpdate
from app.models import models
from fastapi import Depends
from app.api import deps


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_product(self,
                       db: Session,
                       obj_in: ProductCreate,
                       category_id: str,
                       ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.product.append(category_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_shop_id(
            self, db: Session, product_id: UUID, category_id: UUID) -> Product:
        return db.query(self.model).filter(Product.product_id == product_id,
                                           ProductCategory.category_id == category_id
                                           ).all()


product = CRUDProduct(Product)
