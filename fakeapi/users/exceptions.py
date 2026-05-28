from dataclasses import dataclass

from fastapi import HTTPException
from fastapi import status


@dataclass
class UserNotFoundError(HTTPException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found."


@dataclass
class EmailAlreadyExistsError(HTTPException):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Email already exists in this workspace."
