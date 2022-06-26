"""
 Parse new tweets for all accounts from file (data/twitter_urts.txt)
"""
import os
import json
import logging
from typing import List
from datetime import datetime as dt, timedelta as td

from airflow.decorators import dag, task
from airflow.macros import ds_add
from airflow.models import Variable

from utils.common import read_file
from twitter.parser import TwitterAPI


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": td(minutes=15),
    'execution_timeout': td(minutes=60),
}
environment = {
    'AIRFLOW_HOME': Variable.get('AIRFLOW_HOME'),
    'BEARER_TOKEN': Variable.get('BEARER_TOKEN'),
    'TWITTER_URLS_PATH': os.path.join(Variable.get('AIRFLOW_HOME'), 'data', 'twitter_urls.txt'),
    'DATASET': 'twitter',
}


@dag(
    f'{environment["DATASET"]}_operations',
    default_args=default_args,
    schedule_interval='15 1 * * *',
    catchup=True,  # False = prevent airflow from backfilling dag runs
    start_date=dt(2022, 6, 15),
    max_active_runs=1,
    doc_md=__doc__
)
def etl():
    # Task1
    @task(pool='default_pool')
    def get_twitter_accounts(file_name: str = environment['TWITTER_URLS_PATH']) -> List[str]:
        """get all Twitter accounts from file"""
        output = [i.split('/')[-1] for i in read_file(file_name)]
        return output

    # Task2
    @task(pool='external')
    def twitter_account_info(accounts: List[str]) -> List[str]:
        """get Twitter accounts ID"""
        tw = TwitterAPI(bearer_token=environment['BEARER_TOKEN'])

        output = []
        for acc in accounts:
            ep = f'2/users/by/username/{acc}'
            data = tw.fetch(endpoint=ep)
            output.append(data['data']['id'])

        return output

    # Task3
    @task(pool='external')
    def get_tweets(account_ids: List[str], **kwargs) -> int:
        """download current day tweets"""
        tw = TwitterAPI(bearer_token=environment['BEARER_TOKEN'])
        cnt = 0

        for account_id in account_ids:
            # find all tweets' ids
            ep = f'2/users/{account_id}/tweets'
            params = {
                'max_results': 100,  # 5-100
                'exclude': 'replies,retweets',
                'tweet.fields': 'created_at,id',
                'start_time': kwargs['ds'] + 'T00:00:00.000Z',
                'end_time': ds_add(kwargs['ds'], 1) + 'T00:00:00.000Z',
            }
            logging.info(ep)
            logging.info(params)

            # todo: if more than 100 tweets per day, will need to implement page pagination
            data = tw.fetch(endpoint=ep, params=params)
            logging.info(data)

            # get full info about each tweet and save it to json_newline file
            if data['meta']['result_count'] > 0:
                file_name = f'{environment["AIRFLOW_HOME"]}/data/{account_id}_{kwargs["ds"]}.json'

                with open(file_name, 'w') as f:
                    output = [x['id'] for x in data['data']]
                    cnt += len(output)

                    for tw_id in output:
                        tw_ep = '1.1/statuses/show.json'
                        tw_params = {
                            'id': tw_id
                        }
                        tw_info = tw.fetch(endpoint=tw_ep, params=tw_params)
                        # add HOT if more than 100 likes per tweet
                        tw_info['is_hot'] = True if tw_info['favorite_count'] > 100 else False
                        f.write(json.dumps(tw_info))
                        f.write('\n')

        return cnt

    # run
    tw_accounts = get_twitter_accounts()
    acc_ids = twitter_account_info(tw_accounts)
    get_tweets(acc_ids)


data_dag = etl()
