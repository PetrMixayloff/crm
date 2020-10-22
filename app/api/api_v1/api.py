from typing import Any
from app.api import deps
from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import login, users, shop
from app.models import models

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])


@api_router.get("/meta")
def get_meta(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Get schemas meta data.
    """
    return deps.get_all_schemas_models()
