from typing import Dict, Union, Any, List, Optional
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Orders, OrdersProductsRelation, OrdersRawRelation
from app import schemas
from app import crud


class CRUDOrder(CRUDBase[Orders, schemas.OrderCreate, schemas.OrderUpdate]):

    def create_order(self, db: Session, *, obj_in: schemas.OrderCreate) -> Orders:
        order_id = uuid4()
        if obj_in.client_id is None:
            client = crud.client.create(db, obj_in.client)
            obj_in.client_id = client.id
        for product in obj_in.products:
            

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDOrder(Orders)
