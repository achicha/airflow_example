# First-time build can take upto 10 mins.

FROM apache/airflow:2.2.5-python3.8
ENV AIRFLOW_HOME=/opt/airflow

################################
USER root
RUN apt-get update -qq && apt-get install nano -qq

WORKDIR $AIRFLOW_HOME
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

################################
USER $AIRFLOW_UID
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
