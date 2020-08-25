from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.models import Shop
from app.schemas import ShopCreate, ShopUpdate


class CRUDShop(CRUDBase[Shop, ShopCreate, ShopUpdate]):
    def create(self, db: Session, *, obj_in: ShopCreate) -> Shop:
        db_obj = Shop(
            name=obj_in.name,
            address=obj_in.address,
            staff=obj_in.staff
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Shop, obj_in: Union[ShopUpdate, Dict[str, Any]]
    ) -> Shop:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, login: str, password: str) -> Optional[Shop]:
        ahop = self.get_by_login(db, login=login)
        if not ahop:
            return None
        if not verify_password(password, ahop.password):
            return None
        return ahop

    def is_active(self, ahop: Shop) -> bool:
        return ahop.is_active

    def is_superahop(self, ahop: Shop) -> bool:
        return ahop.is_superahop


shop = CRUDShop(Shop)
