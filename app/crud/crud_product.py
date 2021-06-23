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
        if len(obj_in.raw) > 0:
            obj_in_data = jsonable_encoder(obj_in, exclude={'raw', 'products'})
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.flush()
            for raw in obj_in.raw:
                raw.product_id = db_obj.id
                raw_in_data = jsonable_encoder(raw)
                raw_obj = ProductRawRelation(**raw_in_data)
                db.add(raw_obj)
        # else:
        #     products = obj_in.products
        #     obj_in_data = jsonable_encoder(obj_in, exclude={'products'})
        #     db_obj = ProductSet(**obj_in_data)  # type: ignore
        #     db.add(db_obj)
        #     db.flush()
        #     for product_set_rel in products:
        #         product_set_rel.product_set_id = db_obj.id
        #         product_set_rel_in_data = jsonable_encoder(product_set_rel)
        #         product_set_rel_obj = ProductSetRelation(**product_set_rel_in_data)
        #         db.add(product_set_rel_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_product(self, db: Session, *, db_obj: Union[Product, ProductSet],
                       obj_in: Union[schemas.ProductUpdate, schemas.ProductSetUpdate]
                       ) -> Union[Product, ProductSet]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if isinstance(db_obj, Product):
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
        else:
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


product = CRUDProduct(Product)
