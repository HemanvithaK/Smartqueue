import uuid
from datetime import datetime
from pydantic import BaseModel


class JobCreateRequest(BaseModel):
    job_type: str  # "dummy" | "summarize" | "classify" | "extract"
    payload: dict


class JobResponse(BaseModel):
    id: uuid.UUID
    job_type: str
    status: str
    payload: dict
    result: dict | None
    error_message: str | None
    created_at: datetime

    class Config:
        from_attributes = True