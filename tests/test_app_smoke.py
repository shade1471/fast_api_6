from http import HTTPStatus
from random import randint

import requests


def test_app_run(app_url: str):
    response = requests.get(f'{app_url}/status')
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['database']
    assert body['status'] == 'App run successful'


def test_smoke_users(users_endpoint: str):
    response = requests.get(f'{users_endpoint}')
    assert response.status_code == HTTPStatus.OK


def test_smoke_user(users_endpoint: str):
    user_id = randint(1, 12)
    response = requests.get(f"{users_endpoint}/{user_id}")
    assert response.status_code == HTTPStatus.OK
