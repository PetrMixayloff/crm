from typing import Dict, Union, Any, List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product, ProductRawRelation
from app import schemas
from app import crud


class CRUDProduct(CRUDBase[Product, schemas.ProductCreate, schemas.ProductUpdate]):

    def create_product(self, db: Session, *, obj_in: schemas.ProductCreate,
                       raws: List[schemas.ProductRawRelationCreate]) -> Product:

        obj_in_data = jsonable_encoder(obj_in)
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
                       obj_in: schemas.ProductUpdate,
                       raw_relation_create: List[schemas.ProductRawRelationCreate] = [],
                       raw_relation_update: List[schemas.ProductRawRelationUpdate] = [],
                       raw_relation_delete: List[schemas.ProductRawRelation] = []
                       ) -> Product:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if raw_relation_create is not None:
            for raw in raw_relation_create:
                raw.product_id = update_data['id']
                raw_in_data = jsonable_encoder(raw)
                raw_obj = ProductRawRelation(**raw_in_data)
                db.add(raw_obj)

        if raw_relation_update is not None:
            for raw in raw_relation_update:
                product_raw_relation = crud.product_raw_relation.get(db, id=raw.id)
                setattr(product_raw_relation, 'quantity', raw.quantity)
                setattr(product_raw_relation, 'raw_id', raw.raw_id)

        if raw_relation_delete is not None:
            for raw in raw_relation_delete:
                crud.product_raw_relation.remove(db, id=raw.id)

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
