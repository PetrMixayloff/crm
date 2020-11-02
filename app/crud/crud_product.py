from typing import Dict, Union, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app import crud


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

    def get_multi_product(
            self, db: Session, shop_id: str, category_id: str, skip: int = 0, take: int = 100, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        product = db.query(self.model).filter(self.model.shop_id == shop_id,
                                              self.model.category_id == category_id)
        if filter is not None:
            product = self.filter_query(product, filter)
        product = product.offset(skip).limit(take).all()
        data = {
            'totalCount': len(product),
            'data': product
        }
        return data

    def get_multi_product_by_id(
            self, db: Session, shop_id: str, category_id: str, product_id: str,
            skip: int = 0, take: int = 100, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        product_category_by_id = db.query(self.model).filter(self.model.shop_id == shop_id,
                                                             self.model.category_id == category_id,
                                                             self.model.id == product_id)
        if filter is not None:
            product_category_by_id = self.filter_query(product_category_by_id, filter)
        product_category_by_id = product_category_by_id.offset(skip).limit(take).all()
        data = {
            'totalCount': len(product_category_by_id),
            'data': product_category_by_id
        }
        return data


product = CRUDProduct(Product)
