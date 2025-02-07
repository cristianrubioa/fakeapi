from fastapi import APIRouter

from fakeapi.tasks.data import tasks_db
from fakeapi.tasks.models import TaskModel

router = APIRouter()


@router.get("/", response_model=list[TaskModel])
async def get_tasks():
    return tasks_db
