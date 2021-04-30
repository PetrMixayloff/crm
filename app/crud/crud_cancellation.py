from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Cancellation, CancellationRecord
from app import crud, schemas


class CRUDCancellation(CRUDBase[Cancellation, schemas.CancellationCreate, schemas.CancellationUpdate]):

    def create_cancellation(self, db: Session, *, obj_in: schemas.CancellationCreate) -> Cancellation:

        obj_in_data = jsonable_encoder(obj_in)
        records = obj_in_data.pop('records')
        cancelation_obj = self.model(**obj_in_data)  # type: ignore
        db.add(cancelation_obj)
        db.flush()
        for record in records:
            record['cancellation_id'] = cancelation_obj.id
            record['shop_id'] = cancelation_obj.shop_id
            record_obj = CancellationRecord(**record)  # type: ignore
            db.add(record_obj)
            raw = crud.raw.get(db=db, id=record['raw_id'])
            if raw is not None and raw.quantity > 0:
                if raw.quantity > record['quantity']:
                    raw.quantity -= record['quantity']
                    raw.available_quantity -= record['quantity']
                else:
                    raw.available_quantity -= raw.quantity
                    raw.quantity = 0
                db.add(raw)
        db.commit()
        db.refresh(cancelation_obj)
        return cancelation_obj


cancellation = CRUDCancellation(Cancellation)
