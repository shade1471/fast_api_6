import math
from http import HTTPStatus

import pytest

from app.database.users import count_users
from utils.fast_api_app import FastApiApp


@pytest.fixture(scope='module', autouse=True)
def current_count_users() -> int:
    return count_users()


@pytest.fixture(scope='function')
def app(env: str):
    return FastApiApp(env)


@pytest.mark.parametrize('size', (1, 3, 5))
def test_count_users_on_page_by_size_change(app: FastApiApp, size: int):
    """Проверить количество пользователей на странице, при разном параметре size"""
    response = app.get_all_users(params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    items = body['items']
    assert len(items) == size
    assert body['size'] == size
    assert body['page'] == 1
    assert body['total']


@pytest.mark.parametrize('size', (1, 6, 12, 100))
def test_count_page_by_size_change(app: FastApiApp, current_count_users: int, size: int):
    """Проверить количество страниц, при разном параметре size"""
    response = app.get_all_users(params={'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    actual_pages = body['pages']
    expected_pages = math.ceil(current_count_users / size)

    assert actual_pages == expected_pages
    assert body['page'] == 1
    assert body['size'] == size
    assert body['total']


@pytest.mark.parametrize('page', (1, 2, 3))
def test_count_users_on_page_by_size_const(app: FastApiApp, current_count_users: int, page: int):
    """Проверить количество пользователей на каждой полной странице при фиксированном size"""
    size = 2
    expected_pages = math.ceil(current_count_users / size)

    response = app.get_all_users(params={'page': page, 'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body['page'] == page
    assert len(body['items']) == 2
    assert body['size'] == size
    assert body['pages'] == expected_pages


def test_results_items_by_page_change(app: FastApiApp):
    """Проверить, что возвращаются разные данные при разных значениях page"""
    size = 4

    response_one = app.get_all_users(params={'page': 1, 'size': size})
    assert response_one.status_code == HTTPStatus.OK
    body_one = response_one.json()
    response_two = app.get_all_users(params={'page': 2, 'size': size})
    assert response_two.status_code == HTTPStatus.OK
    body_two = response_two.json()

    users_ids_one = {user['id'] for user in body_one['items']}
    users_ids_two = {user['id'] for user in body_two['items']}

    assert not (users_ids_one & users_ids_two)
    assert body_one['page'] != body_two['page']
    assert body_one['size'] == body_two['size'] == size
