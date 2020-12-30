from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Cancellation, CancellationRecord
from app import crud, schemas


class CRUDCancellation(CRUDBase[Cancellation, schemas.CancellationCreate, schemas.CancellationUpdate]):

    def create_cancellation(self, db: Session, *, obj_in: schemas.CancellationCreate
                           ) -> Cancellation:

        obj_in_data = jsonable_encoder(obj_in)
        records = obj_in_data.pop('records')
        obj_in_data['id'] = uuid4()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        for cancellation_records in records:
            cancellation_records['cancellation_id'] = db_obj.id
            cancellation_records_obj = CancellationRecord(**cancellation_records)  # type: ignore
            db.add(cancellation_records_obj)
            db.commit()
            raw_remains = crud.raw_remains_detail.get(db, id=cancellation_records['rawremainsdetail_id'])
            raw_remains_data = jsonable_encoder(raw_remains)
            setattr(raw_remains, 'quantity', raw_remains_data['quantity'] - cancellation_records['quantity'])
            db.add(raw_remains)
            db.commit()
        db.refresh(db_obj)
        return db_obj


cancellation = CRUDCancellation(Cancellation)
