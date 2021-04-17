from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import reflection
from app.core.config import settings
from pydantic import PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLALCHEMY_ASYNC_DATABASE_URI = AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            path=f"/{settings.POSTGRES_DB}",
        )
async_engine = create_async_engine(SQLALCHEMY_ASYNC_DATABASE_URI, pool_pre_ping=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

inspector = reflection.Inspector.from_engine(engine)
