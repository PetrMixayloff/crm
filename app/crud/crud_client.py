from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Client, Address
from app.schemas import ClientCreate, ClientUpdate
from uuid import uuid4


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):

    def create(self, db: Session, *, obj_in: ClientCreate) -> Client:
        obj_in.address_id = uuid4()
        if obj_in.address is not None:
            address_data = jsonable_encoder(obj_in.address)
            address_data['id'] = obj_in.address_id
            address_obj = Address(**address_data)
            db.add(address_obj)
        obj_in_data = jsonable_encoder(obj_in, exclude=set('address'))
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Client, obj_in: ClientUpdate
    ) -> Client:
        if obj_in.address is not None:
            address_obj = db.query(Address).filter(Address.id == obj_in.address_id).first()
            address_data = jsonable_encoder(obj_in.address)
            address_data['id'] = obj_in.address_id
            if address_obj is not None:
                for field in address_data:
                    if hasattr(address_obj, field):
                        setattr(address_obj, field, address_data[field])
            else:
                address_obj = Address(**address_data)
            db.add(address_obj)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


client = CRUDClient(Client)
