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


def test_twitter_api_header(tw):
    """ token is not empty """
    assert tw.HEADERS['Authorization'] != 'Bearer '
    assert tw.HEADERS['Authorization'] != 'Bearer write_your_token_here'


@pytest.mark.parametrize('account', ['elonmusk'])
@pytest.mark.parametrize('account_id', ['44196397'])
def test_twitter_api_account_id(tw, account, account_id):
    """get account_id by using api"""
    account_data = tw.account_info(account)
    acc_id = account_data['id']
    assert acc_id == account_id


@pytest.mark.parametrize('account_id', ['44196397'])
@pytest.mark.parametrize('tweet_id', ['1539275446625476614'])
@pytest.mark.parametrize('start_time', ['2022-06-21T00:00:00.000Z'])
@pytest.mark.parametrize('end_time', ['2022-06-22T00:00:00.000Z'])
def test_twitter_api_tweet_id(tw, account_id, tweet_id, start_time, end_time):
    """get recent tweet_id"""
    tweets_data = tw.get_tweets(account_id, start_time, end_time)
    tw_id = tweets_data['data'][0]['id']
    assert tw_id == tweet_id


@pytest.mark.parametrize('tweet_id', ['1539275446625476614'])
@pytest.mark.parametrize('tweet_text', ['https://t.co/YhpHKcCYXz'])
def test_twitter_api_tweet_info(tw, tweet_id, tweet_text):
    """get tweet full info"""
    tw_info = tw.tweet_info(tweet_id)
    assert tw_info['text'] == 'https://t.co/YhpHKcCYXz'
