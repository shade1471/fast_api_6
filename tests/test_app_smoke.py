from http import HTTPStatus
from random import randint

import pytest

from utils.fast_api_app import FastApiApp


@pytest.fixture(scope='function')
def app(env: str):
    return FastApiApp(env)


def test_app_run(app: FastApiApp):
    response = app.get_status()
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['database']
    assert body['status'] == 'App run successful'


def test_smoke_users(app: FastApiApp):
    response = app.get_status()
    assert response.status_code == HTTPStatus.OK


def test_smoke_user(app: FastApiApp):
    user_id = randint(1, 12)
    response = app.get_user_by_id(user_id)
    assert response.status_code == HTTPStatus.OK
