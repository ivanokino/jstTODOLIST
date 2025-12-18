from sqlalchemy import select, delete, update
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models.TaskModels import TaskModel
from database import Base, SessionDep
from schemas.TaskSchemas import TaskSchema
from api.users import security
router = APIRouter()


@router.post("/setup_db")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@router.post("/tasks", dependencies=[Depends(security.access_token_required)])
async def add_task(data: TaskSchema, session: SessionDep):
    new_task = TaskModel(
        name=data.name, text=data.text, status=data.status, deadline=data.deadline
    )
    if new_task.name == "":
        raise HTTPException(status_code=400, detail="name is empty")
    session.add(new_task)
    await session.commit()
    return {"ok": True}


@router.get("/tasks", dependencies=[Depends(security.access_token_required)])
async def get_tasks(session: SessionDep):
    query = select(TaskModel)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(status_code=404, detail="list is empty")

    return tasks


@router.get("/tasks/{id}", dependencies=[Depends(security.access_token_required)])
async def get_task(session: SessionDep, id: int):
    query = select(TaskModel).where(TaskModel.id == id)
    result = await session.execute(query)
    tasks = result.scalars().one_or_none()
    if not tasks:
        raise HTTPException(status_code=404, detail="cant find task with this ID")
    return tasks


@router.delete("/tasks/{id}", dependencies=[Depends(security.access_token_required)])
async def delete_task(session: SessionDep, id: int):
    query_check = select(TaskModel).where(TaskModel.id == id)
    result_check = await session.execute(query_check)
    task = result_check.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    query = delete(TaskModel).where(TaskModel.id == id)
    result = await session.execute(query)
    await session.commit()

    return {"is_OK": True}


@router.put("/tasks/{id}", dependencies=[Depends(security.access_token_required)])
async def update_task(id: int, session: SessionDep, data: TaskSchema):
    query = select(TaskModel).where(TaskModel.id == id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="task isn't found")

    new_task = {
        "name": data.name,
        "text": data.text,
        "status": data.status,
        "deadline": data.deadline,
    }
    query = update(TaskModel).where(TaskModel.id == id).values(**new_task)
    await session.execute(query)
    await session.commit()
    return {"ok": True}


@router.get("/tasks_page", dependencies=[Depends(security.access_token_required)])
async def get_page(session: SessionDep, limit: int, offset: int):
    query = select(TaskModel).limit(limit).offset(offset)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if tasks is None:
        raise HTTPException(status_code=404, detail="tasks isn't found")
    return tasks
