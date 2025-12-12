from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
##
from Schemas import TaskADDshema, TaskSchema
from Models import TaskModel, Base
##
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, delete, update
from Models import TaskModel



app = FastAPI()
engine = create_async_engine("sqlite+aiosqlite:///database.db")

async def get_session():
    async with new_session() as session:
        yield session

new_session = async_sessionmaker(engine, expire_on_commit=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]



@app.post("/setup_db")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True}


@app.post("/tasks")
async def add_task(data:TaskADDshema, session:SessionDep):
    new_task = TaskModel(
        name = data.TaskName, 
        text=data.TaskText,
        status=data.TaskStatus,
        deadline = data.TashDeadline
    )
    if new_task.name=="":
        raise HTTPException(status_code=400, detail="name is empty")
    session.add(new_task)
    await session.commit()
    return {"ok":True}


@app.get("/tasks")
async def get_tasks(session:SessionDep):
    query = select(TaskModel)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(status_code=404, detail="list is empty")
    
    return tasks


@app.get("/tasks/{id}")
async def get_task(session:SessionDep, id:int):
    query = select(TaskModel).where(TaskModel.id==id)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(status_code=404, detail="cant find task with this ID")
    return tasks


@app.delete("/tasks/{id}")
async def remove_task(session:SessionDep, id:int):
    query = delete(TaskModel).where(TaskModel.id==id)
    
    result = await session.execute(query)
    task = result.scalar_one_or_none
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    await session.commit()
    return {"is_OK":True}


@app.put("/tasks/{id}")
async def update_task(id:int, session:SessionDep, data:TaskADDshema):
    query = select(TaskModel).where(TaskModel.id == id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="task isn't found")

    new_task = {
        "name": data.TaskName,
        "text": data.TaskText,
        "status":data.TaskStatus,
        "deadline":data.TashDeadline
    }
    query = update(TaskModel)\
            .where(TaskModel.id == id)\
            .values(**new_task)
    await session.execute(query)
    await session.commit()
    return {"ok":True}


@app.get("/tasks_page")
async def get_page(session:SessionDep, limit:int, offset:int):
    query = select(TaskModel).limit(limit).offset(offset)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if tasks is None:
        raise HTTPException(status_code=404, detail="tasks isn't found")
    return tasks