from typing import Any
from app.api import deps
from fastapi import APIRouter, Depends

from app.api.api_v1.endpoints import login, users, shop, product, product_category, raw, \
    raw_category
from app.models import models

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(product_category.router, prefix="/product_category", tags=["product_category"])
api_router.include_router(raw.router, prefix="/raw", tags=["raw"])
api_router.include_router(raw_category.router, prefix="/raw_category", tags=["raw_category"])


@api_router.get("/meta")
def get_meta(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Get schemas meta data.
    """
    return deps.get_all_schemas_models()
