from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str


class ExtractRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    name: str
    age: Optional[int] = None
    email: Optional[str] = None
    job: Optional[str] = None
