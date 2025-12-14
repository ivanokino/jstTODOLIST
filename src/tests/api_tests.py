import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from database import init_db
from models.TaskModels import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
task = TaskModel(
            name="Test Task",
            text="text",
            status="status",
            deadline="2027-12-31"
        )
schema_task = {"name":"Test Task",
    "text":"text",
    "status":"status",
    "deadline":"2027-12-31"}

async def setup_bd():
    await init_db()
    async with AsyncSession(engine) as session:
        session.add(task)
        await session.commit()

@pytest.mark.asyncio
async def test_get_task():
    await setup_bd()
    
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        
        response = await ac.get("/tasks")
        assert response.status_code in [200, 400]

@pytest.mark.asyncio
async def test_add_task():
    await setup_bd()

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        
        response = await ac.post("/tasks", json=schema_task)
        assert response.status_code == 200
@pytest.mark.asyncio
async def test_update_task():
    await setup_bd()
    
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        response = await client.get("/tasks")
        task_id = response.json()[0]["id"]
        upgr_resp = await client.put(f"/tasks/{task_id}", json=schema_task)
        assert upgr_resp.status_code == 200
        
@pytest.mark.asyncio
async def test_delete_task():
    await setup_bd()
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        
        response = await client.get("/tasks")
        tasks_id = response.json()[0]['id']

        del_resp = await client.delete(f"/tasks/{tasks_id}")
        assert del_resp.status_code == 200

