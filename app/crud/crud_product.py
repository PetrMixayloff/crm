from typing import Dict, Union, Any, List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Product, ProductRawRelation, ProductSetRelation
from app import schemas
from app import crud
from app.schemas import ProductRawRelationUpdate


class CRUDProduct(CRUDBase[Product, schemas.ProductCreate, schemas.ProductUpdate]):

    def create_product(self, db: Session, *, obj_in: schemas.ProductCreate) \
            -> Product:
        obj_in_data = jsonable_encoder(obj_in, exclude={'raw', 'products'})
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        if len(obj_in.raw) > 0:
            for raw in obj_in.raw:
                raw.product_id = db_obj.id
                raw_in_data = jsonable_encoder(raw)
                raw_obj = ProductRawRelation(**raw_in_data)
                db.add(raw_obj)
        elif len(obj_in.products) > 0:
            for product_set_rel in obj_in.products:
                product_set_rel.product_set_id = db_obj.id
                product_set_rel_in_data = jsonable_encoder(product_set_rel)
                product_set_rel_obj = ProductSetRelation(**product_set_rel_in_data)
                db.add(product_set_rel_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_product(self, db: Session, *, db_obj: Product,
                       obj_in: schemas.ProductUpdate
                       ) -> Product:
        if len(obj_in.raw_to_delete) > 0:
            self.delete_nested_raw(db=db, raw_ids=obj_in.raw_to_delete)
        if len(obj_in.products_to_delete) > 0:
            self.delete_nested_products(db=db, product_set_id=obj_in.product_set_id,
                                        product_ids=obj_in.products_to_delete)
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if len(obj_in.raw) > 0:
            for raw in obj_in.raw:
                if isinstance(raw, ProductRawRelationUpdate):
                    product_raw_relation = crud.product_raw_relation.get(db, id=raw.id)
                    setattr(product_raw_relation, 'quantity', raw.quantity)
                    setattr(product_raw_relation, 'raw_id', raw.raw_id)
                    setattr(product_raw_relation, 'standard_id', raw.standard_id)
                else:
                    raw.product_id = update_data['id']
                    raw_in_data = jsonable_encoder(raw)
                    raw_obj = ProductRawRelation(**raw_in_data)
                    db.add(raw_obj)
        elif len(obj_in.products) > 0:
            for product_set_rel in obj_in.products:
                if product_set_rel.product_set_id is not None:
                    product_set_relation = db.query(ProductSetRelation) \
                        .filter(ProductSetRelation.product_id == product_set_rel.product_id,
                                ProductSetRelation.product_set_id == product_set_rel.product_set_id).first()
                    setattr(product_set_relation, 'quantity', product_set_rel.quantity)
                    db.add(product_set_relation)
                else:
                    product_set_rel.product_set_id = db_obj.id
                    product_set_rel_in_data = jsonable_encoder(product_set_rel)
                    product_set_rel_obj = ProductSetRelation(**product_set_rel_in_data)
                    db.add(product_set_rel_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_nested_raw(self, db: Session, raw_ids: List[str]):
        db.execute(
            ProductRawRelation.delete().where(ProductRawRelation.c.id.in_(raw_ids))
        )

    def delete_nested_products(self, db: Session, product_set_id: str, product_ids: List[str]):
        db.execute(
            ProductRawRelation.delete().where(ProductSetRelation.c.product_set_id == product_set_id,
                                              ProductSetRelation.c.product_id.in_(product_ids))
        )


product = CRUDProduct(Product)
