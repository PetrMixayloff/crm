from typing import Optional
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app import crud
from app.models.models import User, Permissions
from app.schemas import UserCreate, UserUpdate, PermissionsCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_phone(self, db: Session, *, phone: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.phone == phone).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        user_permissions = PermissionsCreate(user_id=db_obj.id)
        crud.permissions.create(db=db, obj_in=user_permissions)
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        if obj_in.password is not None:
            obj_in.password = get_password_hash(obj_in.password)
        else:
            obj_in.password = db_obj.password
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, phone: str, password: str) -> Optional[User]:
        user = self.get_by_phone(db, phone=phone)
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

    # new async crud functions
    async def get_by_phone_async(self, async_db: AsyncSession, phone: str) -> Optional[User]:
        result = await async_db.execute(select(self.model).where(self.model.phone == phone))
        return result.scalar()

    async def create_async(self, async_db: AsyncSession, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['permissions'] = None
        db_obj = self.model(**obj_in_data)
        async_db.add(db_obj)
        await async_db.flush()
        permissions_in = PermissionsCreate(user_id=db_obj.id)
        db_obj.permissions = await crud.permissions.create_async(async_db=async_db, obj_in=permissions_in)
        return db_obj


user = CRUDUser(User)
