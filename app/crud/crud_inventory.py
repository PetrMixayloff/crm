from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Inventory, InventoryRecord
from app import crud, schemas


class CRUDInventory(CRUDBase[Inventory, schemas.InventoryCreate, schemas.InventoryUpdate]):

    def create_inventory(self, db: Session, *, obj_in: schemas.InventoryCreate) -> Inventory:
        obj_in_data = jsonable_encoder(obj_in)
        records = obj_in_data.pop('records')
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        for record in records:
            record['inventory_id'] = db_obj.id
            record_obj = InventoryRecord(**record)  # type: ignore
            db.add(record_obj)
            differ = record['quantity'] - record['old_quantity']
            if differ != 0:
                raw_remains_detail = crud.raw_remains_detail.get_multi(db=db, shop_id=obj_in.shop_id,
                                                                       filter=['raw_id', '=', record['raw_id']])
                if raw_remains_detail['totalCount'] > 0:
                    if differ > 0:
                        remains = raw_remains_detail['data'][0]
                        remains.quantity += differ
                        remains.remark = f'Увеличено на {differ} шт. ' \
                                         f'Причина: инвентаризация номер {db_obj.number}'
                        db.add(remains)
                    else:
                        for remains in raw_remains_detail['data']:
                            if remains.quantity + differ > 0:
                                remains.quantity += differ
                                remains.remark = f'Уменьшено на {differ} шт. ' \
                                                 f'Причина: инвентаризация номер {db_obj.number}'
                                db.add(remains)
                                break
                            else:
                                differ += remains.quantity
                                remains.remark = f'Уменьшено на {remains.quantity} шт. ' \
                                                 f'Причина: инвентаризация номер {db_obj.number}'
                                remains.quantity = 0
                                db.add(remains)
                raw = crud.raw.get(db=db, id=record.get('raw_id'))
                if raw is not None:
                    raw.quantity += differ
                    raw.available_quantity += differ
                    db.add(raw)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inventory = CRUDInventory(Inventory)
