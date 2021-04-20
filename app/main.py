from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import crud, schemas
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.session import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup():
    """
    Initialization on startup
    """
    try:
        db = SessionLocal()
        superuser = crud.user.get_by_phone(db, phone=settings.FIRST_SUPERUSER)
        if not superuser:
            user_in = schemas.SuperUserCreate(
                phone=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True
            )
            crud.user.create(db, obj_in=user_in)

            user_in = schemas.AdminCreate(
                phone=settings.DEVELOP_ADMIN,
                password=settings.DEVELOP_ADMIN_PASSWORD,
                full_name='develop shop admin',
                position='Владелец',
                is_staff=False
            )
            crud.user.create(db, obj_in=user_in)

            admin = crud.user.get_by_phone(db=db, phone=settings.DEVELOP_ADMIN)
            shop_in = schemas.ShopCreate(
                name=settings.DEVELOP_SHOP_NAME,
                is_active=True,
                address='Develop shop address'
            )
            crud.shop.create_with_owner(db, obj_in=shop_in, owner=admin)
    finally:
        db.close()


app.include_router(api_router, prefix=settings.API_V1_STR)
