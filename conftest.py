import os

import dotenv
import pytest


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="rc")


@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def app_url() -> str:
    return os.getenv("APP_URL")


@pytest.fixture(scope='session')
def users_endpoint() -> str:
    app_url = os.getenv("APP_URL")
    return f'{app_url}/api/users'
