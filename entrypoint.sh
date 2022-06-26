#!/bin/bash

AIRFLOW_HOME=$(pwd)

export AIRFLOW_HOME
export AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
export AIRFLOW__CORE__PLUGINS_FOLDER=$AIRFLOW_HOME/plugins
export AIRFLOW__CORE__BASE_LOG_FOLDER=$AIRFLOW_HOME/logs

airflow db upgrade
airflow users create -r Admin -u admin -p admin -e admin@example.com -f admin -l airflow
airflow variables set DAGS_FOLDER $AIRFLOW_HOME
airflow variables set BEARER_TOKEN $BEARER_TOKEN
airflow pools set external 5 "fetch data from external API"

airflow webserver
# airflow scheduler
