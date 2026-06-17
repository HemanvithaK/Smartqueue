import uuid
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    org_name: str
    org_slug: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str
    tenant_id: uuid.UUID

    class Config:
        from_attributes = True