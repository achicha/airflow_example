"""
 Parse new tweets for all accounts from file (data/twitter_urts.txt)
"""
import json
import logging
from typing import List, Dict
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
    'DAGS_PATH': Variable.get('DAGS_FOLDER'),
    'BEARER_TOKEN': Variable.get('BEARER_TOKEN'),
    'DATASET': 'twitter',
}


@dag(
    f'{environment["DATASET"]}_operations',
    default_args=default_args,
    schedule_interval='15 1 * * *',
    catchup=False,  # False = prevent airflow from backfilling dag runs
    start_date=dt(2022, 1, 1),
    max_active_runs=1,
    doc_md=__doc__
)
def etl():
    # Task1
    @task(pool='default_pool')
    def get_twitter_accounts() -> List[str]:
        """get all Twitter accounts from file"""
        file_with_tw_urls = f'{environment["DAGS_PATH"]}/data/twitter_urls.txt'
        output = [i.split('/')[-1] for i in read_file(file_with_tw_urls)]
        return output

    # Task2
    @task(pool='external')
    def twitter_account_info(accounts: List[str]) -> List[Dict]:
        """get Twitter accounts info (ID)"""
        tw = TwitterAPI(bearer_token=environment['BEARER_TOKEN'])

        output = []
        for acc in accounts:
            account_ep = f'2/users/by/username/{acc}'
            account_data = tw.fetch(endpoint=account_ep)
            output.append(account_data['data'])

        return output

    tw_accounts = get_twitter_accounts()
    twitter_account_info(tw_accounts)


data_dag = etl()
