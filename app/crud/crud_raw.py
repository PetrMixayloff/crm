from typing import Dict, Union, Any, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Raw
from app.schemas import RawCreate, RawUpdate
from fastapi.encoders import jsonable_encoder


class CRUDRaw(CRUDBase[Raw, RawCreate, RawUpdate]):

    def get_multi_by_category_id(
            self, db: Session, category_id: str, skip: int = 0, take: int = 1000000, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        raws = db.query(self.model).filter(self.model.is_active.is_(True),
                                           self.model.category_id == category_id)
        if filter is not None:
            raws = self.filter_query(raws, filter)
        raws = raws.offset(skip).limit(take).all()
        data = {
            'totalCount': len(raws),
            'data': raws
        }
        return data

    def create_raw(self, db: Session, raw_in: RawCreate):
        raw_in_data = jsonable_encoder(raw_in)
        raw_obj = self.model(**raw_in_data)  # type: ignore
        if raw_obj.piece_unit is not None:
            piece_raw_obj = self.create_piece(raw_in)
            db.add(piece_raw_obj)
            db.flush()
            raw_obj.piece_raw_id = piece_raw_obj.id
        db.add(raw_obj)
        db.commit()
        return raw_obj

    def update_raw(self, db: Session, raw_in: RawUpdate, raw_obj: Raw):
        if raw_in.piece_raw_id is None and raw_in.piece_unit is not None:
            piece_raw_obj = self.create_piece(raw_in)
            db.add(piece_raw_obj)
            db.flush()
            raw_in.piece_raw_id = str(piece_raw_obj.id)
        return super().update(db, obj_in=raw_in, db_obj=raw_obj)

    def delete_raw(self, db: Session, _id: str):
        raw = self.get(db=db, id=_id)
        if raw.piece_raw_id is not None:
            piece_raw = self.get(db=db, id=raw.piece_raw_id)
            piece_raw.is_active = False
            db.add(piece_raw)
        raw.is_active = False
        db.add(raw)
        db.commit()

    def create_piece(self, raw_in: Union[RawCreate, RawUpdate]) -> Raw:
        return self.model(shop_id=raw_in.shop_id,
                          category_id=raw_in.category_id,
                          name=raw_in.name + '(разб.)',
                          article_number=raw_in.article_number + '-Р'
                          if raw_in.article_number is not None else None,
                          manufacturer=raw_in.manufacturer,
                          unit=raw_in.piece_unit,
                          helium_consumption=raw_in.helium_consumption,
                          description=raw_in.description,
                          image=raw_in.image)


raw = CRUDRaw(Raw)
