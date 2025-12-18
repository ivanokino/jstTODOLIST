from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_session() as session:
        yield session

new_session = async_sessionmaker(engine, expire_on_commit=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


users_engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_users_session = async_sessionmaker(users_engine, expire_on_commit=False)

async def get_users_session():
    async with new_users_session() as session:
        yield session


UsersSessionDep = Annotated[AsyncSession, Depends(get_users_session)]
