from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from ..models.models import User
from ..utils import is_none_or_space

router = APIRouter()


@router.get("/users/{uuid}")
async def get_user(uuid: UUID):
    user = await User.get_or_404(uuid)
    return user.to_dict()


class UserModel(BaseModel):
    login: str
    password: str
    full_name: str
    is_superuser: bool = False
    is_staff: bool = True
    remark: str = None


@router.post("/users")
async def add_user(user: UserModel):
    if is_none_or_space(user.login) or is_none_or_space(user.password):
        raise HTTPException(status_code=409, detail='Не указан логин и/или пароль')

    rv = await User.create(login=user.login,
                           password=user.password,
                           full_name=user.full_name,
                           is_superuser=user.is_superuser,
                           is_staff=user.is_staff,
                           remark=user.remark
                           )
    return rv.to_dict()


@router.delete("/users/{uuid}")
async def delete_user(uuid: UUID):
    user = await User.get_or_404(uuid)
    await user.delete()
    return dict(id=uuid)


def init_app(app):
    app.include_router(router)