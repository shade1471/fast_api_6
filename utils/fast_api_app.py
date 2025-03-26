from requests import Response

from config import Server
from utils.base_session import BaseSession


class FastApiApp:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def get_user_by_id(self, user_id: int) -> Response:
        return self.session.get(f'/api/users/{user_id}')

    def get_all_users(self, params=None) -> Response:
        return self.session.get('/api/users/', params=params)

    def create_user(self, user: dict) -> Response:
        return self.session.post('/api/users/', json=user)

    def update_user(self, user_id: int, user: dict) -> Response:
        return self.session.patch(f'/api/users/{user_id}', json=user)

    def delete_user(self, user_id: int) -> Response:
        return self.session.delete(f'/api/users/{user_id}')

    def get_status(self) -> Response:
        return self.session.get('/status')
