import logging


class Server:
    def __init__(self, env):
        if env not in ['dev', 'beta', 'rc']:
            raise ValueError('Не верная передача параметра --env=[dev, beta, rc]')
        self.app = {
            "dev": "http://127.0.0.1:80",
            "beta": "http://127.0.0.1:8001",
            "rc": "http://127.0.0.1:8000",
        }[env]
