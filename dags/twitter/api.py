import os
import logging
import requests
from retry import retry
from typing import TypedDict, Dict, List


class AccountInfo(TypedDict):
    id: str
    name: str
    username: str


class Tweets(TypedDict):
    data: List[Dict]
    meta: Dict


class TwitterAPI:
    def __init__(self, bearer_token: str):
        self.HEADERS = {
            'Authorization': f'Bearer {bearer_token}',
            'content-type': 'application/json',
        }

    @retry(exceptions=Exception, tries=5, jitter=(3, 7), logger=None)
    def _fetch(self, endpoint: str, params: dict = None) -> Dict:
        """fetch Twitter API"""
        base = 'https://api.twitter.com'

        url = os.path.join(base, endpoint)
        logging.info(url)

        r = requests.get(url, headers=self.HEADERS, params=params)
        r.raise_for_status()

        return r.json()

    def account_info(self, account: str) -> AccountInfo:
        """
            get user account info by name
        :param account: 'elonmusk'
        :return: AccountInfo
        """
        ep = f'2/users/by/username/{account}'
        logging.info(ep)
        return self._fetch(endpoint=ep)['data']

    def get_tweets(self, account_id: str, start_time: str, end_time: str) -> Tweets:
        """
            get tweets by account
        :param account_id: '44196397'
        :param start_time: '2022-06-21T00:00:00.000Z'
        :param end_time: '2022-06-22T00:00:00.000Z'
        :return: Tweets
        """
        # todo: if more than 100 tweets per day, will need to implement page pagination
        ep = f'2/users/{account_id}/tweets'
        params = {
            'max_results': 100,  # 5-100
            'exclude': 'replies,retweets',
            'tweet.fields': 'created_at,id',
            'start_time': start_time,
            'end_time': end_time,
        }
        logging.info(ep)
        logging.info(params)
        return self._fetch(endpoint=ep, params=params)

    def tweet_info(self, tweet_id: str) -> Dict:
        """
            get tweet details
        :param tweet_id: '1539275446625476614'
        :return: Dict with tweet's info
        """
        ep = '1.1/statuses/show.json'
        params = {
            'id': tweet_id
        }
        return self._fetch(endpoint=ep, params=params)
