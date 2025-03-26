from http import HTTPStatus
from random import randint

from utils.fast_api_app import FastApiApp


def test_app_run(env: str):
    app = FastApiApp(env)
    response = app.get_status()
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['database']
    assert body['status'] == 'App run successful'


def test_smoke_users(env: str):
    app = FastApiApp(env)
    response = app.get_status()
    assert response.status_code == HTTPStatus.OK


def test_smoke_user(env: str):
    app = FastApiApp(env)
    user_id = randint(1, 12)
    response = app.get_user_by_id(user_id)
    assert response.status_code == HTTPStatus.OK
