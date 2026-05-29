from dataclasses import dataclass

from fastapi import HTTPException
from fastapi import status


@dataclass
class ProjectNotFoundError(HTTPException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Project not found."
