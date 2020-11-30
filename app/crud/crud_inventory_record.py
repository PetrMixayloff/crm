from typing import Dict, Union, Any, List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import InventoryRecord, RawRemainsDetail
from app import schemas
from app import crud


class CRUDInventoryRecord(CRUDBase[InventoryRecord, schemas.InventoryRecordCreate, schemas.InventoryRecordUpdate]):

    def create_inventory_record(self, db: Session, *, obj_in: schemas.InventoryRecordCreate,
                                raw_remains_update: List[schemas.RawRemainsDetailUpdate]) -> InventoryRecord:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        for quantity in raw_remains_update:
            raw_remains_detail = crud.raw_remains_detail.get(db, id=quantity.id)
            setattr(raw_remains_detail, 'quantity', quantity.quantity)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inventory_record = CRUDInventoryRecord(InventoryRecord)
