from typing import Dict, Union, Any, List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Orders, OrdersProductsRelation, OrdersProductsRawRelation
from app import schemas
from app import crud


class CRUDOrder(CRUDBase[Orders, schemas.OrderCreate, schemas.OrderUpdate]):

    def create(self, db: Session, *, obj_in: schemas.OrderCreate) -> Orders:
        try:
            if obj_in.client_id is None:
                client = crud.client.create(db, obj_in.client)
                obj_in.client_id = client.id
            obj_in_data = jsonable_encoder(obj_in, exclude={'products', 'client'})
            db_obj = self.model(**obj_in_data)  # type: ignore
            db_obj.id = uuid4()
            db.add(db_obj)
            for order_product in obj_in.products:
                order_product.order_id = db_obj.id
                if len(order_product.raw) == 0:
                    product_obj = crud.product.get(db=db, id=order_product.product_id)
                    for raw in product_obj.raw:
                        order_product.raw.append(schemas.OrdersProductsRawRelationCreate(raw_id=raw.raw_id,
                                                                                         standard_id=raw.standard_id,
                                                                                         quantity=raw.quantity))
                order_product_in_data = jsonable_encoder(order_product, exclude={'raw'})
                order_product_obj = OrdersProductsRelation(**order_product_in_data)
                order_product_obj.id = uuid4()
                db.add(order_product_obj)
                for raw in order_product.raw:
                    raw.order_product_id = order_product_obj.id
                    order_product_raw_in_data = jsonable_encoder(raw)
                    order_product_raw_obj = OrdersProductsRawRelation(**order_product_raw_in_data)
                    db.add(order_product_raw_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception:
            db.rollback()
            raise


order = CRUDOrder(Orders)
