run:

1. download repo files `git clone git@github.com:achicha/airflow_example.git`
2. go to airflow directory `cd airflow_example`
3. add twitter `BEARER_TOKEN=` to `.env`
4. start local airflow:
   ```shell
    docker-compose up --build -d
    ```
5. open airflow web `http://0.0.0.0:8080/` with `admin/admin` credentials
6. run tests:
   ```shell
    docker ps                             # get container_id from dwh_scheduler
    docker exec -it container_id bash     # go inside running container
    cd /opt/airflow                       # move to airflow directory
    export PYTHONPATH="$(pwd)"            # add dags folder to variables
    cd /opt/airflow/tests                 # move to test directory
    pytest                                # run all tests
    pytest -k test_twitter_api_account_id # or run specific test
   ```
7. exit:
    ```shell
    docker-compose down                 # stop local airflow service
    ```