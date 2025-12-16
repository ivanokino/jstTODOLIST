from authx import AuthXConfig, AuthX
from fastapi import APIRouter, HTTPException
from schemas.UserSchemas import UserSchema
from database import UsersSessionDep, users_engine, Base
from sqlalchemy import select
from models.UserModels import UserModel

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "wkHf2u324keg2s4o1s"
config.JWT_ACCESS_COOKIE_NAME = "JWT_access_token"
config.JWT_ACCESS_COOKIE_PATH = "/"
security = AuthX(config=config)


@router.post("/setup_users_db")
async def setup_db():
    async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True}


@router.post("/register")
async def create_user(data: UserSchema, session: UsersSessionDep):
    query = select(UserModel).where(UserModel.username == data.name)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User is already exist")
    

    new_user = UserModel(
        username=data.name,
    )
    new_user.set_password(data.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return{
        "name":new_user.username,
        "id":new_user.user_id
    }