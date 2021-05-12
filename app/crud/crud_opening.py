from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Opening, RawRemainsDetail, RawRemainsLog
from app import crud, schemas
from app.core.constants import RawRemainsActions


class CRUDOpening(CRUDBase[Opening, schemas.OpeningCreate, schemas.OpeningUpdate]):

    def create_opening(self, db: Session, obj_in: schemas.OpeningCreate) -> Opening:
        raw = crud.raw.get(db=db, id=obj_in.raw_id)
        raw_remains_detail_obj = db.query(RawRemainsDetail)\
            .filter(RawRemainsDetail.id == obj_in.raw_remains_details_id).first()
        if raw is None or raw_remains_detail_obj is None or raw.quantity <= 0:
            raise HTTPException(
                status_code=409,
                detail="Ошибка создания документа разборки.",
            )
        opening_in_data = jsonable_encoder(obj_in)
        opening_obj = self.model(**opening_in_data)  # type: ignore
        db.add(opening_obj)
        db.flush()
        # обновляем количество в детализированной таблице остатов
        raw_remains_detail_obj.quantity -= 1 if raw_remains_detail_obj.quantity > 0 else 0
        db.add(raw_remains_detail_obj)
        # обновляем количество сырья в БД
        if raw.quantity > 0:
            raw.quantity -= 1
            raw.available_quantity -= 1
        else:
            raw.available_quantity = 0 - raw.reserved
            raw.quantity = 0
        db.add(raw)
        # делаем запись в таблицу истории остатков по сырью
        raw_remains_log_obj = RawRemainsLog(
            shop_id=raw.shop_id,
            raw_id=raw.id,
            arrival=True,
            action=RawRemainsActions.opening.value,
            number=opening_obj.number,
            date=opening_obj.date,
            quantity=1,
            total=raw.quantity
        )
        db.add(raw_remains_log_obj)
        db.commit()
        return opening_obj


opening = CRUDOpening(Opening)
