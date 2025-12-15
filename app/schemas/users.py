from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#  User Schemas

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    password: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str