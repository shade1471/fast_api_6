from typing import Iterable, Type

from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from app.models.user import UserData, UserCreateData
from ..database.engine import engine


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)


def get_users() -> Iterable[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return session.exec(statement).all()


def count_users():
    with Session(engine) as session:
        return session.exec(func.count(UserData.id)).scalar()


def create_user(user: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def create_user_from_api_request(user: UserCreateData) -> UserData:
    """
    Создание пользователя в БД, с моделью по API
    """
    with Session(engine) as session:
        new_user = UserData(email='', first_name=user.name, last_name='', avatar='', job=user.job)

        return create_user(new_user)


def update_user(user_id: int, user: UserCreateData) -> Type[UserData]:
    with Session(engine) as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.first_name = user.name
        db_user.job = user.job
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()


def get_max_user_id() -> int:
    """
    Получение текущего максимального id по таблице пользователей
    """
    with Session(engine) as session:
        max_id = session.exec(func.max(UserData.id)).scalar()

        return max_id
