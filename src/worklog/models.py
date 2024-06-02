from pydantic import BaseModel


class NotFoundException(BaseModel):
    detail: str = "The record not found"
