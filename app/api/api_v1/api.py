from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, shop, product, product_category

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(product_category.router, prefix="/product_category", tags=["product_category"])
