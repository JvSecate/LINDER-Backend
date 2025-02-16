from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    message: str
    status_code: int
    body: T | dict = {}
