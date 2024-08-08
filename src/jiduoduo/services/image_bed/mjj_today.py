import logging
import re
from datetime import datetime

import requests

from jiduoduo.services.image_bed.base import ImageBedService

logger = logging.getLogger(__name__)


class MjjTodayImageBedService(ImageBedService):
    base_url: str = 'https://mjj.today'  # https://img.hmvod.cc/
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0'

    def __init__(self, auth_token: str | None = None):
        self.auth_token = auth_token

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

    def get_auth_token(self) -> str:
        if self.auth_token:
            return self.auth_token

        url = self.get_url('/')
        headers = self.get_headers()

        response = self.session.get(url, headers=headers)
        html = response.text

        match = re.search(r'auth_token = "(?P<auth_token>.*)";', html)
        if match:
            return match.group('auth_token')
        return ''

    def upload(self, image) -> dict:
        url = self.get_url('/json')
        headers = self.get_headers({'Referer': url})

        auth_token = self.get_auth_token()
        logger.info(f'auth_token={auth_token}')

        data = {
            'type': 'file',
            'action': 'upload',
            'timestamp': str(int(datetime.now().timestamp() * 1000)),
            'auth_token': auth_token,
            'expiration': '',
            'nsfw': '0',
        }
        files = {'source': image}

        response = self.session.post(
            url, data=data, files=files, headers=headers,
        )
        logger.info(f'response.text={response.text}')

        return response.json()


r = '''
{
    "status_code": 200,
    "success": {
        "message": "image uploaded",
        "code": 200
    },
    "image": {
        "name": "46d0abbecede15e6629b4bd44ed6a940",
        "extension": "jpeg",
        "size": 11832,
        "width": "108",
        "height": "120",
        "date": "2024-07-22 00:10:48",
        "date_gmt": "2024-07-21 16:10:48",
        "title": "30 avatar middle",
        "description": null,
        "nsfw": "0",
        "storage_mode": "datefolder",
        "md5": "6335651ee356e856810ba6174366e073",
        "source_md5": null,
        "original_filename": "30_avatar_middle.jpg",
        "original_exifdata": "{\"FileName\":\"chvtempSgUEyX\",\"FileDateTime\":\"1721578248\",\"FileSize\":\"11832\",\"FileType\":\"2\",\"MimeType\":\"image\\\/jpeg\",\"SectionsFound\":\"\",\"COMPUTED\":{\"html\":\"width=\\\"108\\\" height=\\\"120\\\"\",\"Height\":\"120\",\"Width\":\"108\",\"IsColor\":\"1\"},\"IPTC\":[],\"width\":\"108\",\"height\":\"120\"}",
        "views": "0",
        "category_id": null,
        "chain": "5",
        "thumb_size": "6107",
        "medium_size": "0",
        "expiration_date_gmt": null,
        "likes": "0",
        "is_animated": "0",
        "is_approved": "1",
        "is_360": "0",
        "file": {
            "resource": {
                "type": "url"
            }
        },
        "id_encoded": "j3BSa8",
        "filename": "46d0abbecede15e6629b4bd44ed6a940.jpeg",
        "mime": "image\/jpeg",
        "url": "https:\/\/ice.frostsky.com\/2024\/07\/22\/46d0abbecede15e6629b4bd44ed6a940.jpeg",
        "ratio": 0.9,
        "size_formatted": "11.8 KB",
        "url_viewer": "https:\/\/mjj.today\/i\/j3BSa8",
        "path_viewer": "\/i\/j3BSa8",
        "url_short": "https:\/\/mjj.today\/i\/j3BSa8",
        "image": {
            "filename": "46d0abbecede15e6629b4bd44ed6a940.jpeg",
            "name": "46d0abbecede15e6629b4bd44ed6a940",
            "mime": "image\/jpeg",
            "extension": "jpeg",
            "url": "https:\/\/ice.frostsky.com\/2024\/07\/22\/46d0abbecede15e6629b4bd44ed6a940.jpeg",
            "size": 11832
        },
        "thumb": {
            "filename": "46d0abbecede15e6629b4bd44ed6a940.th.jpeg",
            "name": "46d0abbecede15e6629b4bd44ed6a940.th",
            "mime": "image\/jpeg",
            "extension": "jpeg",
            "url": "https:\/\/ice.frostsky.com\/2024\/07\/22\/46d0abbecede15e6629b4bd44ed6a940.th.jpeg",
            "size": "6107"
        },
        "display_url": "https:\/\/ice.frostsky.com\/2024\/07\/22\/46d0abbecede15e6629b4bd44ed6a940.jpeg",
        "display_width": "108",
        "display_height": "120",
        "views_label": "\u6b21\u6d4f\u89c8",
        "likes_label": "\u6536\u85cf",
        "how_long_ago": "1 \u79d2\u524d",
        "date_fixed_peer": "2024-07-21 16:10:48",
        "title_truncated": "30 avatar middle",
        "title_truncated_html": "30 avatar middle",
        "is_use_loader": false,
        "delete_url": "https:\/\/mjj.today\/i\/j3BSa8\/delete\/2b23293aa6f770d8807d46498f05bc59c1bc3f8d4f304cff"
    },
    "request": {
        "type": "file",
        "action": "upload",
        "timestamp": "1721578247807",
        "auth_token": "d0e59297d3231dbaa7866df3ee0d74cd25647d05",
        "expiration": "",
        "nsfw": "0"
    },
    "status_txt": "OK"
}
'''
