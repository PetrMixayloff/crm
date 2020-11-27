from typing import Dict, Union, Any, List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import InvoiceRecord, RawRemainsDetail
from app import schemas
from app import crud



class CRUDInvoiceRecord(CRUDBase[InvoiceRecord, schemas.InvoiceRecordCreate, schemas.InvoiceRecordUpdate]):

    def create_invoice_record(self, db: Session, *, obj_in: schemas.InvoiceRecordCreate,
                              raw_remains_create: List[schemas.RawRemainsDetailCreate]) -> InvoiceRecord:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        for invoice in raw_remains_create:
            invoice.invoice_id = db_obj.invoice_id
            invoice.raw_id = db_obj.raw_id
            invoice.quantity = db_obj.quantity
            invoice.total = db_obj.total
            invoice_in_data = jsonable_encoder(invoice)
            invoice_obj = RawRemainsDetail(**invoice_in_data)
            db.add(invoice_obj)
            db.commit()

        return db_obj

    def update_invoice_record(self, db: Session, *, db_obj: InvoiceRecord,
                              obj_in: schemas.InvoiceRecordUpdate,
                              raw_remains_update: List[schemas.RawRemainsDetailUpdate]
                              ) -> InvoiceRecord:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        for invoice in raw_remains_update:
            raw_remains_detail = crud.raw_remains_detail.get(db, id=invoice.id)
            setattr(raw_remains_detail, 'quantity', invoice.quantity)
            setattr(raw_remains_detail, 'raw_id', invoice.raw_id)
            setattr(raw_remains_detail, 'invoice_id', invoice.invoice_id)
            setattr(raw_remains_detail, 'price', invoice.price)
            setattr(raw_remains_detail, 'total', invoice.total)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


invoice_record = CRUDInvoiceRecord(InvoiceRecord)
