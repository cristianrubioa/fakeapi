from fastapi import APIRouter

from fakeapi.tasks.models import TaskModel
from fakeapi.tasks.provider import tasks_db

router = APIRouter()


@router.get("/", response_model=list[TaskModel])
async def get_tasks():
    return tasks_db
