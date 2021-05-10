from typing import Optional, Union, Any, Dict
from uuid import uuid4
from sqlalchemy.sql.functions import count, func
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app import crud
from app.models.models import User, Permissions
from app.schemas import UserCreate, UserUpdate, PermissionsCreate, PermissionsUpdate


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

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        permissions = update_data.pop('permissions')
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        permissions_in_base = crud.permissions.get(db, id=permissions['id'])
        setattr(permissions_in_base, 'orders', permissions['orders'])
        setattr(permissions_in_base, 'products', permissions['products'])
        setattr(permissions_in_base, 'raw', permissions['raw'])
        setattr(permissions_in_base, 'clients', permissions['clients'])
        setattr(permissions_in_base, 'clients', permissions['clients'])
        setattr(permissions_in_base, 'staff', permissions['staff'])
        setattr(permissions_in_base, 'warehouse', permissions['warehouse'])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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

    async def get_multi_async(self, async_db: AsyncSession, shop_id: str, skip: int = 0, take: int = 1000000,
                              sort: str = None, filter: Union[str, list] = None) -> Dict[str, Union[int, Any]]:

        stm = select(self.model).where(self.model.shop_id == shop_id)
        if filter is not None:
            stm = self.filter_stm(stm, filter)
        total_stm = select([func.count()]).select_from(stm)
        stm = stm.offset(skip).limit(take)
        result = await async_db.execute(stm)
        total = await async_db.execute(total_stm)
        data = {
            'totalCount': total.scalar(),
            'data': result.scalars().all()
        }
        return data

    async def create_async(self, async_db: AsyncSession, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        obj_in_data = jsonable_encoder(obj_in)
        user_obj = self.model(**obj_in_data)
        async_db.add(user_obj)
        await async_db.flush()
        permissions_in = PermissionsCreate(user_id=user_obj.id)
        await crud.permissions.create_async(async_db=async_db, obj_in=permissions_in)
        await async_db.refresh(user_obj)
        return user_obj


user = CRUDUser(User)
