import logging
import re

import requests

from jiduoduo.services.image_bed.base import ImageBedService

logger = logging.getLogger(__name__)


class GwwcImageBedService(ImageBedService):
    base_url: str = 'https://img.gwwc.net'
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
        # 　https://img.gwwc.net/

        response = self.session.get(self.get_url('/'))
        logger.info(response.text)

        pattern = 'csrf-token" content="(?P<csrf_token>.*)"'
        csrf_token = re.search(pattern, response.text).group('csrf_token')

        url = self.get_url('/upload')
        headers = self.get_headers({
            'Referer': self.get_url('/'),
            'X-Csrf-Token': csrf_token,
        })

        data = {'strategy_id': 15}
        files = {'file': image}

        response = self.session.post(
            url, data=data, files=files, headers=headers,
        )
        logger.info(f'response.text={response.text}')

        return response.json()


r = '''
{"status":true,
"message":"\u4e0a\u4f20\u6210\u529f",
"data":{"id":1090,
"pathname":"2024\/07\/9QC4kQ.png",
"origin_name":"result.png",
"size":49.8642578125,
"mimetype":"image\/png",
"md5":"8bb47f25e9ed65121cbaf4c3ccca0225",
"sha1":"b136539a03f28b2ae45059678252a337f5b3723a",
"links":{"url":"https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png",
"markdown":"![null](https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png)",
"html":"&lt;img src=\"https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png\" alt=\"result.png\" title=\"result.png\" \/&gt;",
"bbcode":"[null]https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png[\/img]",
"markdown_with_link":"[![null](https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png)](https:\/\/img.gwwc.net\/mjj\/2024\/07\/9QC4kQ.png)",
"thumbnail_url":"https:\/\/img.gwwc.net\/thumbnails\/8bb47f25e9ed65121cbaf4c3ccca0225.png"}}}
'''
