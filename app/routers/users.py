from datetime import datetime
from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlmodel import Session

from app.database import users
from app.models.user import UserData, UserResponse, UserCreateData, UserCreateResponse, UserUpdatedResponse
from ..database.engine import engine
from ..models.support import support_data

router = APIRouter(prefix="/api/users")


@router.get("/", response_model=Page[UserData], status_code=HTTPStatus.OK)
async def get_users() -> Page[UserData]:
    db = Session(engine)
    return paginate(db, select(UserData).order_by(UserData.id))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> Union[UserResponse, JSONResponse]:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={})
    return UserResponse(data=user, support=support_data)


@router.post("/", response_model=UserCreateResponse, status_code=HTTPStatus.CREATED)
async def create_user(user: UserCreateData) -> UserCreateResponse:
    UserCreateData.model_validate(user.model_dump())
    formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    user_db = users.create_user_from_api_request(user)
    return UserCreateResponse(name=user.name, job=user_db.job, id=str(user_db.id), createdAt=formatted_date)


@router.patch("/{user_id}", response_model=UserUpdatedResponse)
async def update_user(user_id: int, user: UserCreateData) -> Union[UserUpdatedResponse, JSONResponse]:
    UserCreateData.model_validate(user.model_dump())
    formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    user_db = users.update_user(user_id, user)
    return UserUpdatedResponse(name=user_db.first_name, job=user_db.job, updatedAt=formatted_date)


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> JSONResponse:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content=None)
