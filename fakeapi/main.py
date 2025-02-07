from fastapi import FastAPI

from fakeapi.tasks.routers import router as tasks_router

app = FastAPI(title="Fake API", version="0.1.0")

app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])


@app.get("/", tags=["Root"])
async def root():
    return {"Hello": "World!"}
