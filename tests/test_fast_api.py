from http import HTTPStatus

import pytest
import requests

from app.database.data import users_data
from app.database.users import get_max_user_id, get_user
from app.models.support import SupportData
from app.models.user import UserData, UserCreateData, UserUpdatedResponse
from utils.fast_api_app import FastApiApp


@pytest.fixture(scope='function')
def app(env: str):
    return FastApiApp(env)


@pytest.fixture(scope='function')
def create_user_id(app: FastApiApp) -> int:
    """Фикстура для создания временного пользователя"""

    new_user = {"name": "tmp user", "job": "PM"}

    response = app.create_user(new_user)
    assert response.status_code == HTTPStatus.CREATED, 'Не удалось создать пользователя'
    current_id = response.json()['id']
    return int(current_id)


class TestGetUser:

    @pytest.mark.parametrize('user_id', [1, 2, 3, 4, 5])
    def test_user_data(self, app: FastApiApp, user_id: int):
        response = app.get_user_by_id(user_id)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        data = body["data"]
        UserData.model_validate(data)
        SupportData.model_validate(body['support'])

        assert data["email"] == users_data[user_id].email
        assert data["first_name"] == users_data[user_id].first_name
        assert data["last_name"] == users_data[user_id].last_name

    def test_response_when_user_not_exist(self, app: FastApiApp):
        user_id = get_max_user_id() + 1
        response = app.get_user_by_id(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        body = response.json()
        assert not body

    @pytest.mark.parametrize('user_id', (0, -1))
    def test_not_valid_value_ids(self, app: FastApiApp, user_id: int):
        response = app.get_user_by_id(user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        body = response.json()
        assert body['detail'] == 'Invalid user id'

    @pytest.mark.parametrize('method_name', ('options', 'head', 'put', 'post'))
    def test_not_allowed_method(self, users_endpoint: str, method_name: str):
        method_dict = {'options': requests.options, 'head': requests.head, 'put': requests.put, 'post': requests.post}
        response = method_dict[method_name](f"{users_endpoint}/1")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestCRUD:

    @pytest.mark.parametrize('user_dict', [
        {"name": "Max", "job": "qa-manual"},
        {'name': 'Alisa', 'job': 'qa-auto'}
    ])
    def test_create_user_post_request(self, app: FastApiApp, user_dict: dict):
        """Создание пользователя"""
        response = app.create_user(user_dict)
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        UserCreateData.model_validate(body)
        assert body['name'] == user_dict['name']
        assert body['job'] == user_dict['job']

        new_user_id = body['id']
        new_user = get_user(new_user_id)
        assert new_user.first_name == user_dict['name']
        assert new_user.job == user_dict['job']

    def test_create_not_valid_user(self, app: FastApiApp):
        """Создание пользователя с невалидными данными"""
        response = app.create_user({'name': 'Alisa', 'job': 1})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT

    def test_update_exist_user(self, app: FastApiApp, create_user_id: int):
        """Обновление существующего пользователя"""
        new_data_user = {"name": "Nikolay", "job": "Super PM"}

        response_update = app.update_user(create_user_id, new_data_user)
        assert response_update.status_code == HTTPStatus.OK
        body = response_update.json()
        UserUpdatedResponse.model_validate(body)
        assert body['name'] == new_data_user['name']
        assert body['job'] == new_data_user['job']

        response_updated_user = app.get_user_by_id(create_user_id)
        assert response_updated_user.status_code == HTTPStatus.OK
        new_body = response_updated_user.json()
        data = new_body["data"]
        UserData.model_validate(data)
        SupportData.model_validate(new_body['support'])

        assert data['first_name'] == new_data_user["name"]
        assert data['job'] == new_data_user["job"]

    def test_update_not_exist_user(self, app: FastApiApp):
        """Обновление не существующего пользователя"""
        new_data_user = {"name": "Maxim", "job": "driver"}
        user_id = get_max_user_id() + 1

        response_update = app.update_user(user_id, new_data_user)

        assert response_update.status_code == HTTPStatus.NOT_FOUND
        assert response_update.json()['detail'] == 'User not found'

    def test_update_not_valid_data(self, app: FastApiApp, create_user_id: int):
        """Обновление существующего пользователя не валидными данными"""
        new_data_user = {"name": "Maxim not valid", "job": 1}

        response_update = app.update_user(create_user_id, new_data_user)
        assert response_update.status_code == HTTPStatus.UNPROCESSABLE_CONTENT

    def test_delete_user(self, app: FastApiApp, create_user_id: int):
        """Удаление существующего пользователя"""
        delete_response = app.delete_user(create_user_id)

        assert delete_response.status_code == HTTPStatus.NO_CONTENT
        assert app.get_user_by_id(create_user_id).status_code == HTTPStatus.NOT_FOUND

    def test_delete_not_exist_user(self, app: FastApiApp):
        """Удаление не существующего пользователя"""
        user_id = get_max_user_id() + 1
        delete_response = app.delete_user(user_id)
        assert delete_response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize('user_id', (0, -1))
    def test_delete_with_not_valid_user_id(self, app: FastApiApp, user_id: int):
        """Удаление пользователя с невалидным id"""
        delete_response = app.delete_user(user_id)
        assert delete_response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
