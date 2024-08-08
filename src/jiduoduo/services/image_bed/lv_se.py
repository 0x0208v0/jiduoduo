import logging

import requests

from jiduoduo.services.image_bed.base import ImageBedService

logger = logging.getLogger(__name__)


class LvSeImageBedService(ImageBedService):
    base_url: str = 'https://lvse.eu.org'
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0'

    def __init__(self):
        self.session = requests.Session()

    def get_url(self, resource: str = '') -> str:
        return f'{self.base_url}{resource}'

    def get_headers(self, headers: dict | None = None) -> dict:
        default_headers = {
            'User-Agent': self.user_agent,
            'Origin': self.base_url,
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'accept-language': "en-US,en;q=0.5",
            'Referer': self.get_url('/'),
        }
        return default_headers | (headers or {})

    def upload(self, image) -> dict:
        url = self.get_url('/upload/localhost')
        headers = self.get_headers({'Referer': self.get_url('/')})

        files = {'file': image}

        response = self.session.post(
            url, files=files, headers=headers,
        )
        logger.info(f'response.text={response.text}')

        return response.json()


r = '''
{"code":200,
"id":"10009",
"imgid":"28d3df6c56451571",
"relative_path":"\/imgs\/2024\/07\/28d3df6c56451571.jpg",
"url":"https:\/\/img.erpweb.eu.org\/imgs\/2024\/07\/28d3df6c56451571.jpg",
"thumbnail_url":"https:\/\/img.erpweb.eu.org\/imgs\/2024\/07\/28d3df6c56451571_thumb.jpg",
"width":640,
"height":640,
"delete":"https:\/\/img.0112233.xyz\/delete\/82f50a3e3825eef9"}
'''
