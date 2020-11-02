from typing import Dict, Union, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app import crud


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):

    def get_multi_by_category_id(
            self, db: Session, category_id: str, skip: int = 0, take: int = 1000000, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        products = db.query(self.model).filter(self.model.is_active.is_(True),
                                               self.model.category_id == category_id)
        if filter is not None:
            products = self.filter_query(products, filter)
        products = products.offset(skip).limit(take).all()
        data = {
            'totalCount': len(products),
            'data': products
        }
        return data


product = CRUDProduct(Product)
