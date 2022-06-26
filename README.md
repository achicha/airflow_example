run:

1. add twitter `BEARER_TOKEN=` to `.env`
2. go to airflow directory `cd /opt/airflow`
3. start local airflow:
   ```shell
    docker-compose up --build -d
    ```
4. open airflow web `http://0.0.0.0:8080/` with `admin/admin` credentials
5. run tests:
   ```shell
    export PYTHONPATH="$(pwd)"
    docker ps                           # get container_id from dwh_scheduler
    docker exec -it container_id bash   # go inside running container
    cd /opt/airflow/tests               # move to test directory
    export 
    pytest                              # run all tests
   ```
6. exit:
    ```shell
    docker-compose down                 # stop local airflow service
    ```