from functools import lru_cache
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from .config import get_settings

settings = get_settings()

# ---------- Mongo ----------
mongo_client: AsyncIOMotorClient | None = None
mongo_db = None

# ---------- SQLAlchemy ----------
sql_engine: AsyncEngine | None = None
SessionFactory: async_sessionmaker[AsyncSession] | None = None

# ---------- Inicialização dinâmica ----------
if settings.backend == "mongo":
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    mongo_db = mongo_client[settings.mongo_db]
else:
    # echo=True mostra queries no log; tire em produção
    sql_engine = create_async_engine(settings.postgres_uri, echo=False, future=True)
    SessionFactory = async_sessionmaker(
        bind=sql_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


# ---------- Helpers que a aplicação importa ----------
def get_mongo_db():
    """
    Retorna a referência do banco Mongo, para quem precisar.
    Levanta erro se BACKEND!=mongo.
    """
    if settings.backend != "mongo":
        raise RuntimeError("BACKEND != mongo")
    return mongo_db


@asynccontextmanager
async def get_sql_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependência FastAPI ou uso manual:
        async with get_sql_session() as session:
            ...
    """
    if settings.backend == "mongo":
        raise RuntimeError("BACKEND == mongo (sem sessão SQL)")

    async with SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise