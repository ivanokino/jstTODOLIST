from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase
engine = create_async_engine("sqlite+aiosqlite:///database.db")

async def get_session():
    async with new_session() as session:
        yield session

new_session = async_sessionmaker(engine, expire_on_commit=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass
