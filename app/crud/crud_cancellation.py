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
        cancelation_obj = self.model(**obj_in_data)  # type: ignore
        db.add(cancelation_obj)
        db.flush()
        for record in records:
            record['cancellation_id'] = cancelation_obj.id
            cancellation_records_obj = CancellationRecord(**record)  # type: ignore
            db.add(cancellation_records_obj)
            db.commit()
            raw_remains = crud.raw_remains_detail.get(db, id=record['rawremainsdetail_id'])
            raw_remains_data = jsonable_encoder(raw_remains)
            setattr(raw_remains, 'quantity', raw_remains_data['quantity'] - record['quantity'])
            db.add(raw_remains)
        db.commit()
        db.refresh(cancelation_obj)
        return cancelation_obj


cancellation = CRUDCancellation(Cancellation)
