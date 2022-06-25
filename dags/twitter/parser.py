import os
import logging
import requests
from retry import retry
from typing import Dict


class TwitterAPI:
    def __init__(self, bearer_token: str):
        self.HEADERS = {
            'Authorization': f'Bearer {bearer_token}',
            'content-type': 'application/json',
        }

    @retry(exceptions=Exception, tries=5, jitter=(3, 7), logger=None)
    def fetch(self, endpoint: str, params: dict = None) -> Dict:
        base = 'https://api.twitter.com'

        url = os.path.join(base, endpoint)
        logging.info(url)

        r = requests.get(url, headers=self.HEADERS, params=params)
        r.raise_for_status()

        return r.json()
