from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from annexa.config.settings import settings

engine = create_async_engine(settings.database_url, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

class Base(AsyncAttrs, DeclarativeBase):
    pass
