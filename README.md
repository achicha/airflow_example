run:

1. add twitter `BEARER_TOKEN=` to `.env`
2. go to airflow directory `cd airflow`
3. start local airflow:
   ```shell
    docker-compose up --build -d
    ```
4. open airflow web `http://0.0.0.0:8080/` with `admin/admin` credentials
5. other docker cmd:
    ```shell
    docker ps # check running containers
    docker exec -it container_id bash   # runs a command in a running container
    docker-compose down                 # stop local airflow service
    ```