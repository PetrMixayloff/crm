from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
from ..models.models import User

router = APIRouter()


@router.get("/users/{uuid}")
async def get_user(uuid: uuid4):
    user = await User.get_or_404(uuid)
    return user.to_dict()


class UserModel(BaseModel):
    login: str
    password: str
    full_name: str
    is_superuser: bool
    is_staff: bool
    remark: str


@router.post("/users")
async def add_user(user: UserModel):
    rv = await User.create(login=user.login,
                           password=user.password,
                           full_name=user.full_name,
                           is_superuser=user.is_superuser,
                           is_staff=user.is_staff,
                           remark=user.remark
                           )
    return rv.to_dict()


@router.delete("/users/{uuid}")
async def delete_user(uuid: uuid4):
    user = await User.get_or_404(uuid)
    await user.delete()
    return dict(id=uuid)


def init_app(app):
    app.include_router(router)