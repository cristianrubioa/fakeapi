from datetime import datetime

from pydantic import BaseModel


class WorkspaceResponseModel(BaseModel):
    id: str
    created_at: datetime
    expires_at: datetime
    extend_count: int
    plan: str


class WorkspaceCountResponseModel(BaseModel):
    count: int
    limit: int
