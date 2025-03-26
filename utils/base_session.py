import logging

import curlify
from requests import Session


class BaseSession(Session):
    def __init__(self, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)

    def request(self, method, url, **kwargs):
        url = self.base_url + url
        response = super().request(method, url, **kwargs)
        logging.info(curlify.to_curl(response.request))
        return response
