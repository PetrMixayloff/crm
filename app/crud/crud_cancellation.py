from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Cancellation, CancellationRecord, RawRemainsDetail, RawRemainsLog
from app import crud, schemas
from app.core.constants import RawRemainsActions


class CRUDCancellation(CRUDBase[Cancellation, schemas.CancellationCreate, schemas.CancellationUpdate]):

    def create_cancellation(self, db: Session, obj_in: schemas.CancellationCreate) -> Cancellation:

        # записываем в базу сущность расходной накладной
        obj_in_data = jsonable_encoder(obj_in)
        records = obj_in_data.pop('records')
        cancellation_obj = self.model(**obj_in_data)  # type: ignore
        db.add(cancellation_obj)
        db.flush()
        for record in records:
            raw = crud.raw.get(db=db, id=record['raw_id'])
            raw_remains_detail_obj = db.query(RawRemainsDetail). \
                filter(RawRemainsDetail.id == record['raw_remains_details_id']).first()
            if raw is None or raw_remains_detail_obj is None or record['quantity'] <= 0:
                db.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Ошибка создания расходной накладной.",
                )
            # записываем в БД позицию в накладной
            record['cancellation_id'] = cancellation_obj.id
            record['shop_id'] = cancellation_obj.shop_id
            record_obj = CancellationRecord(**record)  # type: ignore
            db.add(record_obj)
            # обновляем количество в детализированной таблице остатов
            if raw_remains_detail_obj.quantity > record['quantity']:
                raw_remains_detail_obj.quantity -= record['quantity']
            else:
                raw.raw_remains_detail_obj = 0
            db.add(raw_remains_detail_obj)
            # обновляем количество сырья в БД
            if raw.quantity > record['quantity']:
                raw.quantity -= record['quantity']
                raw.available_quantity -= record['quantity']
            else:
                raw.available_quantity = 0 - raw.reserved
                raw.quantity = 0
            db.add(raw)
            # делаем запись в таблицу истории остатков по сырью
            raw_remains_log_obj = RawRemainsLog(
                shop_id=raw.shop_id,
                raw_id=raw.id,
                arrival=True,
                action=RawRemainsActions.cancel.value,
                number=cancellation_obj.number,
                date=cancellation_obj.date,
                quantity=record['quantity'],
                total=raw.quantity
            )
            db.add(raw_remains_log_obj)
        db.commit()
        db.refresh(cancellation_obj)
        return cancellation_obj


cancellation = CRUDCancellation(Cancellation)
