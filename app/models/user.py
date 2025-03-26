from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from app.models.support import SupportData


class UserData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    first_name: str
    last_name: str
    avatar: str
    job: str


class UserResponse(BaseModel):
    data: UserData
    support: SupportData


class UserCreateData(BaseModel):
    name: str
    job: str


class UserCreateResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UserUpdatedResponse(BaseModel):
    name: str | None = None
    job: str | None = None
    updatedAt: str
