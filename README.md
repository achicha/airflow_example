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
    export PYTHONPATH="$(pwd)"
    docker ps                           # get container_id from dwh_scheduler
    docker exec -it container_id bash   # go inside running container
    cd /opt/airflow/tests               # move to test directory
    export 
    pytest                              # run all tests
   ```
7. exit:
    ```shell
    docker-compose down                 # stop local airflow service
    ```