from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Cancelation, CancelationRecord, RawRemainsDetail
from app import crud, schemas


class CRUDCancelation(CRUDBase[Cancelation, schemas.CancelationCreate, schemas.CancelationUpdate]):

    def create_cancelation(self, db: Session, *, obj_in: schemas.CancelationCreate
                           ) -> Cancelation:

        obj_in_data = jsonable_encoder(obj_in)
        records = obj_in_data.pop('records')
        obj_in_data['id'] = uuid4()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        for cancelation_records in records:
            cancelation_records['cancelation_id'] = db_obj.id
            cancelation_records_obj = CancelationRecord(**cancelation_records)  # type: ignore
            db.add(cancelation_records_obj)
            db.commit()
            raw_remains = crud.raw_remains_detail.get(db, id=cancelation_records['rawremainsdetail_id'])
            raw_remains_data = jsonable_encoder(raw_remains)
            setattr(raw_remains, 'quantity', raw_remains_data['quantity'] - cancelation_records['quantity'])
            db.add(raw_remains)
            db.commit()
        db.refresh(db_obj)
        return db_obj


cancelation = CRUDCancelation(Cancelation)
