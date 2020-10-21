from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_login(self, db: Session, *, login: str) -> Optional[User]:
        return db.query(User).filter(User.login == login).first()

    def check_user_login(self, db: Session, *, login: str) -> Optional[User]:
        return db.query(User).filter(User.login == login).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        if obj_in.password:
            obj_in.password = get_password_hash(obj_in.password)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, login: str, password: str) -> Optional[User]:
        user = self.get_by_login(db, login=login)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_staff(self, user: User) -> bool:
        return user.is_staff

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
