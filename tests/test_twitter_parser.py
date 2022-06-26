import os
import pytest
from dotenv import load_dotenv

from dags.twitter.parser import TwitterAPI


@pytest.fixture()
def tw():
    # load .env to get BEARER_TOKEN
    load_dotenv()
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')

    return TwitterAPI(BEARER_TOKEN)


def test_twitter_parser(tw):
    # token is valid
    assert tw.HEADERS['Authorization'] != 'Bearer '
    assert tw.HEADERS['Authorization'] != 'Bearer write_your_token_here'

    # account_id
    test_account = 'elonmusk'
    account_ep = f'2/users/by/username/{test_account}'
    account_data = tw.fetch(endpoint=account_ep)
    account_id = account_data['data']['id']
    assert account_id == '44196397'

    # recent tweet_id
    tweets_ep = f'2/users/{account_id}/tweets'
    tweets_params = {
        'max_results': 5,   # 5-100
        'exclude': 'replies,retweets',
        'tweet.fields': 'author_id,created_at,id',
        'start_time': '2022-06-21T00:00:00.000Z',
        'end_time': '2022-06-22T00:00:00.000Z',
    }
    tweets_data = tw.fetch(endpoint=tweets_ep, params=tweets_params)
    tweet_id = tweets_data['data'][0]['id']
    assert tweet_id == '1539275446625476614'

    # tweet full info
    tw_ep = '1.1/statuses/show.json'
    tw_params = {
        'id': tweet_id
    }
    tw_info = tw.fetch(endpoint=tw_ep, params=tw_params)
    assert tw_info['text'] == 'https://t.co/YhpHKcCYXz'
