from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers.sql_staging_tables import CreateStagingTablesSQL
from helpers.sql_truncate_staging import TruncateStagingTablesSQL

#import pandas as pd
#import geopandas as gpd



class S3ToStagingWithEnrichment(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 *args, **kwargs):

        super(S3ToStagingWithEnrichment, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Create table if not exists
        try:
            self.log.info(f"Creating table {self.table}.....")
            redshift.run(getattr(CreateStagingTablesSQL, f"create_{self.table}"))
        except Exception as e:
            print(e)
            raise(f"Error creating Table {self.table}, exiting.....")
            
        # Truncate table if it already exists
        self.log.info(f"Truncating data in staging table {self.table}")
        try:
            redshift.run(TruncateStagingTablesSQL.TRUNCATE_STAGING.format(self.table))
        except Exception as e:
            print(e)
            raise(f"Error truncating data in {self.table}, exiting.....")
        
        
        """
        # Enrich data from taxi lookup data
        try:
            self.log.info(f"Fetching data from taxi zone lookup table.....")
            conn = redshift.get_conn()
            cursor = conn.cursor()
            cursor.execute(CreateStagingTablesSQL.select_taxi_zone_lookup_staging)
            #redshift.run(StagingDataQualitySQL.check_number_of_fields.format(self.table))
            sources = cursor.fetchall()
            print(sources)
            
        except Exception as e:
            print(e)
            raise("Unable to fetch taxi_lookup_data")
            
        df_geo = gpd.DataFrame(sources, columns=["geometry",
                                                 "object_id",
                                                 "shape_leng",
                                                 "shape_area",
                                                 "zone",
                                                 "location_id",
                                                 "borough"])
        """

        # Load data from S3 into staging
        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        
        
        # If we are loading a shape file use alternative COPY command
        if self.is_shape:
            formatted_sql = CreateStagingTablesSQL.copy_sql_shape.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
            )
        else:
            formatted_sql = CreateStagingTablesSQL.copy_sql.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.ignore_headers,
                self.delimiter
            )
            
        try:
            redshift.run(formatted_sql)
        except Exception as e:
            print(e)
            raise(f"Error loading data into {self.table}, exiting.....")