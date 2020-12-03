from typing import Dict, Union, Any, List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Invoice, InvoiceRecord, RawRemainsDetail
from app import crud, schemas


class CRUDInvoice(CRUDBase[Invoice, schemas.InvoiceRecordCreate, schemas.InvoiceRecordUpdate]):

    def create_invoice(self, db: Session, *, obj_in: schemas.Invoice,
                       invoice_record_create: List[schemas.InvoiceRecordCreate],
                       raw_remains_create: List[schemas.RawRemainsDetailCreate] = []
                       ) -> Invoice:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        for invoice in invoice_record_create:
            invoice.invoice_id = db_obj.id
            invoice_in_data = jsonable_encoder(invoice)
            invoice_obj = InvoiceRecord(**invoice_in_data)
            db.add(invoice_obj)
            db.commit()

            for record in raw_remains_create:
                record.invoice_id = db_obj.id
                record.raw_id = invoice.raw_id
                record.quantity = invoice.quantity
                record_in_data = jsonable_encoder(record)
                record_obj = RawRemainsDetail(**record_in_data)
                db.add(record_obj)
                db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_invoice(self, db: Session, *, db_obj: Invoice,
                       obj_in: schemas.InvoiceUpdate,
                       invoice_record_update: List[schemas.InvoiceRecordUpdate],
                       raw_remains_update: List[schemas.RawRemainsDetailUpdate]
                       ) -> Invoice:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        for record in invoice_record_update:
            invoice_record = crud.invoice_record.get(db, id=record.id)
            setattr(invoice_record, 'quantity', record.quantity)
            setattr(invoice_record, 'raw_id', record.raw_id)
            setattr(invoice_record, 'invoice_id', record.invoice_id)
            setattr(invoice_record, 'price', record.price)

            for invoice in raw_remains_update:
                raw_remains_detail = crud.raw_remains_detail.get(db, id=invoice.id)
                setattr(raw_remains_detail, 'quantity', record.quantity)
                setattr(raw_remains_detail, 'raw_id', record.raw_id)
                setattr(raw_remains_detail, 'invoice_id', record.invoice_id)
                setattr(raw_remains_detail, 'price', record.price)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


invoice = CRUDInvoice(Invoice)
