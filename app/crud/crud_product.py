from typing import Dict, Union, Any, List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product, ProductRawRelation
from app import schemas
from app import crud


class CRUDProduct(CRUDBase[Product, schemas.ProductCreate, schemas.ProductUpdate]):

    def create_product(self, db: Session, *, obj_in: schemas.ProductCreate) -> Product:

        raws = obj_in.raw
        obj_in_data = jsonable_encoder(obj_in, exclude={'raw'})
        obj_in_data['id'] = uuid4()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        for raw in raws:
            raw.product_id = db_obj.id
            raw_in_data = jsonable_encoder(raw)
            raw_obj = ProductRawRelation(**raw_in_data)
            db.add(raw_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_product(self, db: Session, *, db_obj: Product,
                       obj_in: schemas.ProductUpdate
                       ) -> Product:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        for raw in obj_in.raw:
            if raw.id is not None:
                product_raw_relation = crud.product_raw_relation.get(db, id=raw.id)
                setattr(product_raw_relation, 'quantity', raw.quantity)
                setattr(product_raw_relation, 'raw_id', raw.raw_id)
                setattr(product_raw_relation, 'standard_id', raw.standard_id)
            else:
                raw.product_id = update_data['id']
                raw_in_data = jsonable_encoder(raw)
                raw_obj = ProductRawRelation(**raw_in_data)
                db.add(raw_obj)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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
