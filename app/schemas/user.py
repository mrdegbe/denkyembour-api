from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.enums import RoleEnum
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum


class UserCreate(UserBase):
    is_active: bool
    last_login: Optional[datetime] = None
    department: str


class UserOut(UserBase):
    id: UUID
    department: str
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}
