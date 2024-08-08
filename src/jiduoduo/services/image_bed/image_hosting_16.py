import logging
import random
from string import ascii_letters
from string import digits

import requests

from jiduoduo.services.image_bed.base import ImageBedService

logger = logging.getLogger(__name__)

TOKEN_LENGTH = 32


class ImageHosting16ImageBedService(ImageBedService):
    base_url: str = 'https://i.111666.best'
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0'

    def __init__(self, auth_token: str | None = None):
        self.auth_token = auth_token

        self.session = requests.Session()

    def get_url(self, resource: str = '') -> str:
        return f'{self.base_url}{resource}'

    def get_headers(self, headers: dict | None = None) -> dict:
        auth_token = self.get_auth_token()
        logger.info(f'auth_token={auth_token}')

        default_headers = {
            'User-Agent': self.user_agent,
            'Origin': self.base_url,
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'accept-language': "en-US,en;q=0.5",
            'Referer': self.get_url('/'),
            'Auth-Token': auth_token,
        }
        return default_headers | (headers or {})

    def get_auth_token(self) -> str:
        if self.auth_token:
            return self.auth_token

        return ''.join([random.choice(ascii_letters + digits) for _ in range(TOKEN_LENGTH)])

    def upload(self, image) -> dict:
        url = self.get_url('/image')
        headers = self.get_headers({'Referer': url})

        files = {'abc': image}

        response = self.session.post(
            url, files=files, headers=headers,
        )
        logger.info(f'response.text={response.text}')

        return response.json()


r = '''
{"ok":true, "src":"/image/0hljT6c3OCidEZVKSxnEvF.png"}
'''
