
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator

from airflow.models import Variable
from operators.s3_to_staging import S3ToStaging
#from extract_and_unzip_from_s3 import extract_and_unzip_from_s3
#from extract_and_enrich_from_s3 import extract_and_enrich_from_s3

default_args = {
    'owner': 'tlc',
    'depends_on_past': False,
    'email': ['info@tlc.com', 'darren.foley@ucdconnect.ie'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'redshift_conn_id': 'redshift',
    'aws_credentials_id': 'aws',
    's3_bucket': 'nyc-tlc',
    'start_date': datetime(2020, 3, 1, 0, 0, 0),
    'year': datetime(2020, 3, 1, 0, 0, 0).year,
    'month': datetime(2020, 3, 1, 0, 0, 0).month
}

#HOME_ = "/home/workspace/airflow/dags"
HOME_ = Variable.get("HOME_")
local_bucket = Variable.get("local_bucket")


with DAG(
    "tlc_taxi_base_lookup_etl",
    default_args=default_args,
    start_date=default_args['start_date'],
    #schedule_interval="@monthly",
    schedule_interval=None,
) as dag:
    
    start_operator = DummyOperator(
        task_id="Begin_execution"
    )
      
    load_shape_files_into_staging = S3ToStaging(
        task_id="load_taxi_base_information",
        table="taxi_base_lookup_staging",
        #s3_bucket="tlc-nyc-dwh-df",
        s3_bucket=f"{local_bucket}",
        s3_key="taxi_base/taxi_base_lookup.csv",
        is_shape=False
    )
    
    end_operator = DummyOperator(
        task_id="End_execution"
    )
    
    start_operator >> load_shape_files_into_staging
    load_shape_files_into_staging >> end_operator
    
    

