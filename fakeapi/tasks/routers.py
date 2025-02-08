from fastapi import APIRouter
from fastapi import status

from fakeapi.tasks import services

from fakeapi.tasks.models import TaskCreateModel
from fakeapi.tasks.models import TaskResponseModel
from fakeapi.tasks.models import TaskUpdateModel


router = APIRouter()


@router.post("/", response_model=TaskResponseModel, status_code=status.HTTP_201_CREATED)
async def create_task_route(new_task: TaskCreateModel) -> TaskResponseModel:
    return services.create_task(new_task)


@router.get("/", response_model=list[TaskResponseModel])
async def get_tasks() -> list[TaskResponseModel]:
    return services.get_tasks_list()


@router.get("/{task_id}", response_model=TaskResponseModel)
async def get_task_route(task_id: int) -> TaskResponseModel:
    return services.get_task_by_id(task_id)


@router.patch("/{task_id}", response_model=TaskResponseModel)
async def update_task_partial_route(task_id: int, task_updates: TaskUpdateModel) -> TaskResponseModel:
    return services.update_task_partial(task_id, task_updates)


@router.put("/{task_id}", response_model=TaskResponseModel)
async def update_task_route(task_id: int, new_task_data: TaskUpdateModel) -> TaskUpdateModel:
    return services.update_task(task_id, new_task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int) -> None:
    services.delete_task_by_id(task_id)
