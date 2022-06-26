import os
from pprint import pprint
from dotenv import load_dotenv

from parser import TwitterAPI
from utils.common import read_file


# load .env to get BEARER_TOKEN
load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
test_account = 'elonmusk'
assert isinstance(BEARER_TOKEN, str)


# get twitter accounts from file
file_with_tw_urls = '/Users/andreyev/Documents/Github/airflow_example/data/twitter_urls.txt'
tw_accounts = [i.split('/')[-1] for i in read_file(file_with_tw_urls)]
assert tw_accounts[0] == test_account

# api
tw = TwitterAPI(bearer_token=BEARER_TOKEN)

# account info
account_ep = f'2/users/by/username/{test_account}'
account_data = tw.fetch(endpoint=account_ep)
account_id = account_data['data']['id']
assert account_id == '44196397'
#
# # recent tweets
# account_id = '44196397' # todo: remove
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

# tweet info
# tweet_id = '1539275446625476614' # todo: remove
tw_ep = '1.1/statuses/show.json'
tw_params = {
    'id': tweet_id
}
tw_info = tw.fetch(endpoint=tw_ep, params=tw_params)
assert tw_info['text'] == 'https://t.co/YhpHKcCYXz'
print(account_id, tweet_id)
pprint(tw_info)
