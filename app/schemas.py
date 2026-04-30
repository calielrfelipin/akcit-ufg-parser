from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    status: str


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class ExtractResponse(BaseModel):
    name: str
    age: Optional[int] = None
    email: Optional[str] = None
    job: Optional[str] = None
