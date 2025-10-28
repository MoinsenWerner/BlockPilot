from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    role: str = "admin"


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class InstanceBase(BaseModel):
    name: str
    instance_type: str
    software: str
    version: str
    autostart: bool = False
    autorestart_on_crash: bool = True
    memory_limit: Optional[int] = None
    java_args: Optional[str] = None
    max_players: Optional[int] = None
    port: Optional[int] = None


class InstanceCreate(InstanceBase):
    pass


class InstanceUpdate(BaseModel):
    name: Optional[str] = None
    autostart: Optional[bool] = None
    autorestart_on_crash: Optional[bool] = None
    memory_limit: Optional[int] = None
    java_args: Optional[str] = None
    max_players: Optional[int] = None
    port: Optional[int] = None


class InstanceRead(InstanceBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InstanceLogRead(BaseModel):
    id: int
    message: str
    created_at: datetime

    class Config:
        orm_mode = True


class InstanceDetail(InstanceRead):
    logs: List[InstanceLogRead] = []
