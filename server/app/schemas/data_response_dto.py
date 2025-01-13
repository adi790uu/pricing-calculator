from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# API response object TODO
class ErrorResponse(BaseModel):
    code: int = 1
    message: str


class GenericResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(None, description="Response data")
    error: Optional[ErrorResponse] = Field(None, description="Error details")
