from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Invoice, InvoiceRecord, RawRemainsDetail, RawRemainsLog
from app import crud, schemas
from app.core.constants import RawRemainsActions
from fastapi import HTTPException


class CRUDInvoice(CRUDBase[Invoice, schemas.InvoiceCreate, schemas.InvoiceUpdate]):

    def create_invoice(self, db: Session, *, obj_in: schemas.InvoiceCreate
                       ) -> Invoice:

        # записываем в базу сущность приходной накладной
        invoice_in_data = jsonable_encoder(obj_in)
        records = invoice_in_data.pop('records')
        invoice_obj = self.model(**invoice_in_data)  # type: ignore
        db.add(invoice_obj)
        db.flush()
        for record in records:
            raw = crud.raw.get(db=db, id=record.get('raw_id'))
            if raw is None or record['quantity'] <= 0:
                db.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Ошибка создания приходной накладной.",
                )
            # записываем в БД позицию в накладной
            record['invoice_id'] = invoice_obj.id
            record['shop_id'] = invoice_obj.shop_id
            invoice_records_obj = InvoiceRecord(**record)  # type: ignore
            db.add(invoice_records_obj)
            # обновляем количество в детализированной таблице остатов
            record['invoice'] = True
            record['number'] = invoice_obj.number
            record['date'] = invoice_obj.date
            raw_remains_detail_obj = RawRemainsDetail(**record)  # type: ignore
            db.add(raw_remains_detail_obj)
            # обновляем количество сырья в БД
            if raw.per_pack > 0:
                raw.quantity += record['quantity'] * raw.per_pack
                raw.available_quantity += record['quantity'] * raw.per_pack
            else:
                raw.quantity += record['quantity']
                raw.available_quantity += record['quantity']
            db.add(raw)
            # делаем запись в таблицу истории остатков по сырью
            raw_remains_log_obj = RawRemainsLog(
                shop_id=raw.shop_id,
                raw_id=raw.id,
                arrival=True,
                action=RawRemainsActions.invoice.value,
                number=invoice_obj.number,
                date=invoice_obj.date,
                quantity=record['quantity'],
                total=raw.quantity
            )
            db.add(raw_remains_log_obj)
        db.commit()
        db.refresh(invoice_obj)
        return invoice_obj


invoice = CRUDInvoice(Invoice)
