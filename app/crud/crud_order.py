from typing import Dict, Union, Any, List, Optional
from uuid import uuid4, UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Orders, OrdersProductsRelation, OrdersProductsRawRelation
from app import schemas
from app import crud
from enum import Enum


class Status(Enum):
    new = 'Новый'
    prepared = 'Подготовлен'
    completed = 'Выполнен'
    canceled = 'Отменен'
    on_delivery = 'На доставке'


def create_order_product(db: Session, order_product: schemas.OrdersProductsRelationCreate,
                         order_id: UUID, shop_id: str, status: str):
    order_product.order_id = order_id
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
    for order_product_raw in order_product.raw:
        create_order_product_raw(db=db, order_product_raw=order_product_raw, order_product_id=order_product_obj.id,
                                 shop_id=shop_id, product_quantity=order_product.quantity, status=status)


def create_order_product_raw(db: Session, order_product_raw: schemas.OrdersProductsRawRelationCreate,
                             order_product_id: UUID, shop_id: str, product_quantity: int, status: str):
    order_product_raw.order_product_id = order_product_id
    order_product_raw_in_data = jsonable_encoder(order_product_raw)
    order_product_raw_obj = OrdersProductsRawRelation(**order_product_raw_in_data)
    db.add(order_product_raw_obj)
    raw_remains = crud.raw_remains_detail.get_multi(db=db,
                                                    shop_id=shop_id,
                                                    filter=['raw_id', '=', str(order_product_raw.raw_id)])
    if len(raw_remains) > 0:
        if order_product_raw.standard_id is None:
            if status == Status.new.value:
                raw = crud.raw.get(db=db, id=order_product_raw.raw_id)
                raw.reserved += product_quantity
                db.add(raw)
            else:
                raw_remains[0].quantity -= product_quantity
        else:
            usage_standard = crud.raw_usage_standards.get(db=db, id=order_product_raw.standard_id)
            if status == Status.new.value:
                raw = crud.raw.get(db=db, id=order_product_raw.raw_id)
                raw.reserved += product_quantity * usage_standard.quantity
                db.add(raw)
            else:
                raw_remains[0].quantity -= product_quantity * usage_standard.quantity
        db.add(raw_remains[0])


def update_order_product(db: Session, order_product: schemas.OrdersProductsRelationUpdate,
                         db_obj: OrdersProductsRelation, old_status: str, new_status: str, shop_id: str):
    obj_data = jsonable_encoder(db_obj)
    update_data = order_product.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    for order_product_raw in order_product.raw:
        order_product_raw_obj = crud.order_product_raw.get(db=db, id=order_product_raw.id)
        update_order_product_raw(db=db, order_product_raw=order_product_raw,
                                 db_obj=order_product_raw_obj, product_quantity=order_product.quantity,
                                 old_status=old_status, new_status=new_status, shop_id=shop_id)
    db.add(db_obj)


def update_order_product_raw(db: Session, order_product_raw: schemas.OrdersProductsRawRelationUpdate,
                             db_obj: OrdersProductsRawRelation, product_quantity: int, old_status: str,
                             new_status: str, shop_id: str):
    obj_data = jsonable_encoder(db_obj)
    update_data = order_product_raw.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    raw_remains = crud.raw_remains_detail.get_multi(db=db,
                                                    shop_id=shop_id,
                                                    filter=['raw_id', '=', str(order_product_raw.raw_id)])
    if len(raw_remains) > 0:
        raw = crud.raw.get(db=db, id=order_product_raw.raw_id)
        if old_status == Status.new.value and new_status in [Status.prepared.value,
                                                             Status.completed.value,
                                                             Status.on_delivery.value]:
            if order_product_raw.standard_id is None:
                raw.reserved -= product_quantity
                db.add(raw)
                raw_remains[0].quantity -= product_quantity
            else:
                usage_standard = crud.raw_usage_standards.get(db=db, id=order_product_raw.standard_id)
                raw.reserved -= product_quantity * usage_standard.quantity
                raw_remains[0].quantity -= product_quantity * usage_standard.quantity
        elif old_status == Status.new.value and new_status == Status.canceled.value:
            if order_product_raw.standard_id is None:
                raw.reserved -= product_quantity
            else:
                usage_standard = crud.raw_usage_standards.get(db=db, id=order_product_raw.standard_id)
                raw.reserved -= product_quantity * usage_standard.quantity
        db.add(raw)
        db.add(raw_remains[0])


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
                create_order_product(db=db, order_product=order_product,
                                     order_id=db_obj.id, shop_id=str(obj_in.shop_id), status=obj_in.status)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception:
            db.rollback()
            raise

    def update(
            self,
            db: Session,
            db_obj: Orders,
            obj_in: schemas.OrderUpdate
    ) -> Orders:
        try:
            old_status = db_obj.status
            new_status = obj_in.status
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            for order_product in obj_in.products:
                if isinstance(order_product, schemas.OrdersProductsRelationUpdate):
                    order_product_obj = crud.order_product.get(db=db, id=order_product.id)
                    update_order_product(db=db, order_product=order_product, db_obj=order_product_obj,
                                         old_status=old_status, new_status=new_status, shop_id=str(obj_in.shop_id))
                else:
                    create_order_product(db=db, order_product=order_product,
                                         order_id=db_obj.id, shop_id=str(obj_in.shop_id), status=new_status)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception:
            db.rollback()
            raise


order = CRUDOrder(Orders)
