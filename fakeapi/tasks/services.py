
from fakeapi.tasks.exceptions import ResourceNotFound
from fakeapi.tasks.provider import tasks_db
from fakeapi.tasks.models import TaskCreateModel
from fakeapi.tasks.models import TaskResponseModel
from fakeapi.tasks.models import TaskUpdateModel

def get_tasks_list() -> list[TaskResponseModel]:
    return [TaskResponseModel(**task) for task in tasks_db]


def get_task_by_id(task_id: int) -> TaskResponseModel:
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task is None:
        raise ResourceNotFound()
    return TaskResponseModel(**task)


def create_task(new_task: TaskCreateModel) -> TaskResponseModel:
    new_id = max([task["id"] for task in tasks_db], default=0) + 1
    new_task_data = {
        "id": new_id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
    }
    tasks_db.append(new_task_data)
    return TaskResponseModel(**new_task_data)


def update_task(task_id: int, new_task_data: TaskUpdateModel) -> TaskResponseModel:
    task = get_task_by_id(task_id)
    task_data = {
        "title": new_task_data.title,
        "description": new_task_data.description,
        "status": new_task_data.status,
    }
    task_dict = task.model_dump()
    task_dict.update(task_data)
    return TaskResponseModel(**task_dict)


def update_task_partial(task_id: int, task_updates: TaskUpdateModel) -> TaskResponseModel:
    task = get_task_by_id(task_id)
    task_data = task_updates.model_dump(exclude_unset=True)
    task_dict = task.model_dump()
    task_dict.update(task_data)
    return TaskResponseModel(**task_dict)


def delete_task_by_id(task_id: int) -> None:
    global tasks_db
    if get_task_by_id(task_id) is None:
        raise ResourceNotFound()

    tasks_db = [t for t in tasks_db if t["id"] != task_id]
