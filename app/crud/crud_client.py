from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Client, Address
from app.schemas import ClientCreate, ClientUpdate
from uuid import uuid4


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):

    def get_by_phone(self, db: Session, phone: str) -> Optional[Client]:
        return db.query(self.model).filter(self.model.phone == phone).first()

    def create(self, db: Session, obj_in: ClientCreate) -> Client:
        obj_in_data = jsonable_encoder(obj_in, exclude={'address'})
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        if obj_in.address is not None:
            address_data = jsonable_encoder(obj_in.address)
            address_data['client_id'] = db_obj.id
            address_obj = Address(**address_data)
            db.add(address_obj)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_client(self, db: Session, client_id: str, obj_in: ClientCreate) -> Client:
        db_obj = self.get(db=db, id=client_id)
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
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        return db_obj


client = CRUDClient(Client)
