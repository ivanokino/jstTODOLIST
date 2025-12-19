from fastapi import FastAPI
import uvicorn
from fastapi import APIRouter
from api.tasks import router as tasks_router
from api.users import router as users_router
from fastapi import APIRouter

app = FastAPI()
main_router = APIRouter()
main_router.include_router(tasks_router)
main_router.include_router(users_router)
app.include_router(main_router)


@app.get("/")
async def main():
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True,port=8000)
