import os
import pytest
from dotenv import load_dotenv

from dags.twitter.api import TwitterAPI


@pytest.fixture()
def tw():
    # load .env to get BEARER_TOKEN
    load_dotenv()
    bearer_token = os.getenv('BEARER_TOKEN')

    return TwitterAPI(bearer_token)


def test_twitter_parser(tw):
    # token is valid
    assert tw.HEADERS['Authorization'] != 'Bearer '
    assert tw.HEADERS['Authorization'] != 'Bearer write_your_token_here'

    # account_id
    test_account = 'elonmusk'
    account_data = tw.account_info(test_account)
    account_id = account_data['id']
    assert account_id == '44196397'

    # recent tweet_id
    tweets_data = tw.get_tweets(account_id, '2022-06-21T00:00:00.000Z', '2022-06-22T00:00:00.000Z')
    tweet_id = tweets_data['data'][0]['id']
    assert tweet_id == '1539275446625476614'

    # tweet full info
    tw_info = tw.tweet_info(tweet_id)
    assert tw_info['text'] == 'https://t.co/YhpHKcCYXz'
