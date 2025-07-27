from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.enums import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum


class UserCreate(UserBase):
    department: str


class UserOut(UserBase):
    id: int
    is_active: bool
    department: str
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True
