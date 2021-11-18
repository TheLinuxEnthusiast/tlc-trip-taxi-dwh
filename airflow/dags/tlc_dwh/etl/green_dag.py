from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators import BashOperator

from operators.s3_to_staging import S3ToStaging
from operators.staging_data_quality_check import StagingDataQuality
from operators.load_dependencies import LoadDependencies
from operators.clean_staging_data import CleanStagingData
from operators.load_dimension import LoadDimension
from operators.load_fact import LoadFact
from operators.prod_data_quality_check import ProdDataQualityCheck


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
}


with DAG(
    "tlc_green_taxi_data_etl",
    default_args=default_args,
    #schedule_interval="@monthly",
    schedule_interval=None,
    max_active_runs=1,
) as dag:
    
    start_operator = DummyOperator(
        task_id="Begin_execution"
    )
    
    load_dependencies = LoadDependencies(
        task_id="load_dependencies"
    )
    
    load_taxi_base_data = TriggerDagRunOperator(
        task_id="load_taxi_base_data",
        trigger_dag_id="tlc_taxi_base_lookup_etl",
    )
    
    load_taxi_zone_data = TriggerDagRunOperator(
        task_id="load_taxi_zone_data",
        trigger_dag_id="tlc_taxi_zone_lookup_etl",
    )
    
    load_green_staging_table = S3ToStaging(
        task_id="Load_green_taxi_data_into_staging",
        table="green_staging",
        s3_key="trip data/green_tripdata_{}-{}.csv",
        is_shape=False
    )
    
    green_data_quality_check = StagingDataQuality(
        task_id="Green_data_quality_check",
        table="green_staging"
    )
    
    clean_staging_data = CleanStagingData(
        task_id="clean_staging_data_green",
        table="green_staging",
        schema="public"
    )
    
    load_time_dim = LoadDimension(
        task_id = "load_time_dim",
        source = "green",
        destination="time",
        schema="public"
    )
    
    load_location_dim = LoadDimension(
        task_id = "load_location_dim",
        source = "green",
        destination="location",
        schema="public"
    )
    
    load_vendor_dim = LoadDimension(
        task_id = "load_vendor_dim",
        source = "green",
        destination="vendor",
        schema="public"
    )
    
    load_ratecode_dim = LoadDimension(
        task_id = "load_ratecode_dim",
        source = "green",
        destination="ratecode",
        schema="public"
    )
    
    load_payment_type_dim = LoadDimension(
        task_id = "load_payment_type_dim",
        source = "green",
        destination="payment_type",
        schema="public"
    )
    
    load_taxi_base_dim = LoadDimension(
        task_id = "load_taxi_base_dim",
        source = "green",
        destination="taxi_base",
        schema="public"
    )
    
    load_trip_type_dim = LoadDimension(
        task_id = "load_trip_type_dim",
        source = "green",
        destination="trip_type",
        schema="public"
    )
    
    load_fact = LoadFact(
        task_id = "load_fact",
        source="green",
        schema="public"
    )
    
    prod_data_quality_check = ProdDataQualityCheck(
        task_id="prod_data_quality_check",
        source="green"
    )
    
    end_operator = DummyOperator(
        task_id="End_execution"
    )
    
    start_operator >> [load_taxi_base_data, load_taxi_zone_data, load_dependencies]
    [load_taxi_base_data, load_taxi_zone_data, load_dependencies] >> load_green_staging_table
    load_green_staging_table >> green_data_quality_check
    green_data_quality_check >> clean_staging_data
    clean_staging_data >> [load_time_dim, load_location_dim, load_vendor_dim, load_ratecode_dim, load_payment_type_dim, load_taxi_base_dim, load_trip_type_dim]
    [load_time_dim, load_location_dim, load_vendor_dim, load_ratecode_dim, load_payment_type_dim, load_taxi_base_dim, load_trip_type_dim] >> load_fact
    load_fact >> prod_data_quality_check
    prod_data_quality_check >> end_operator
    