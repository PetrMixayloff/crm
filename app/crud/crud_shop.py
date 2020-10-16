from typing import List, Dict, Optional, Union

from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import User, Shop
from app.schemas import ShopCreate, ShopUpdate


class CRUDShop(CRUDBase[Shop, ShopCreate, ShopUpdate]):
    def create_with_owner(self, db: Session, obj_in: ShopCreate, owner: User) -> Shop:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.users.append(owner)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, owner_id: UUID) -> List[Shop]:
        return db.query(self.model).filter(Shop.owner_id == owner_id).all()


shop = CRUDShop(Shop)
