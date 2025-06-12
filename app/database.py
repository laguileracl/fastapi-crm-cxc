from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

async_session_maker = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

# Dependency para obtener la session
async def get_db():
    async with async_session_maker() as session:
        yield session

# SOLO importa los modelos, SIN dependencias NI get_user_db!
from app.models import client
from app.models import client_comment
from app.models import admin_log
from app.models import user

# Init models
async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# get_user_db se define AL FINAL, y SOLO importa User dentro de la función
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

async def get_user_db(session: AsyncSession = Depends(get_db)):
    from app.models.user import User
    yield SQLAlchemyUserDatabase(session, User)
