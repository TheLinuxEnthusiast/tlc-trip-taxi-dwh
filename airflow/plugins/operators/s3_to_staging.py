from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers.sql_staging_tables import CreateStagingTablesSQL
from helpers.sql_truncate_staging import TruncateStagingTablesSQL

class S3ToStaging(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 delimiter=",",
                 ignore_headers=1,
                 is_shape=False,
                 *args, **kwargs):

        super(S3ToStaging, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers
        self.aws_credentials_id = aws_credentials_id
        self.is_shape=is_shape

    def execute(self, context):
        execution_date = context.get("execution_date")
        print(type(execution_date))
        print(execution_date)
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
        
        # Load data from S3 into staging
        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(execution_date.year, str(execution_date.month).zfill(2))
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