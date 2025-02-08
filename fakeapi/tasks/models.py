from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from fakeapi.settings import settings
from fakeapi.tasks.enums import TaskStatus


class TaskBaseModel(BaseModel):
    title: str = Field(
        ...,
        min_length=settings.TITLE_LIMITS["min"],
        max_length=settings.TITLE_LIMITS["max"],
    )
    description: str = Field(
        ...,
        min_length=settings.DESCRIPTION_LIMITS["min"],
        max_length=settings.DESCRIPTION_LIMITS["max"],
    )
    status: TaskStatus = Field(default=TaskStatus.PENDING)


class TaskCreateModel(TaskBaseModel):
    pass


class TaskUpdateModel(TaskBaseModel):
    title: Optional[str] = Field(
        None,
        min_length=settings.TITLE_LIMITS["min"],
        max_length=settings.TITLE_LIMITS["max"],
    )
    description: Optional[str] = Field(
        None,
        min_length=settings.DESCRIPTION_LIMITS["min"],
        max_length=settings.DESCRIPTION_LIMITS["max"],
    )
    status: Optional[TaskStatus] = None


class TaskResponseModel(TaskBaseModel):
    id: int = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.now)
