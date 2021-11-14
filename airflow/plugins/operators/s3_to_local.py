from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
#from airflow.hooks.S3_hook import S3Hook

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL

class S3ToLocal(BaseOperator):

    @apply_defaults
    def __init__(self,
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="",
                 destination_bucket="",
                 *args, **kwargs):

        super(S3ToLocal, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.destination_bucket=destination_bucket
     
    def execute(self, context):
        hook = S3Hook(aws_conn_id=self.aws_credentials_id)
        
        rendered_key = self.s3_key.format(**context)
        s3_path_source = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        s3_destination = ""
        
        #Create bucket if not exists
        
        
        
        #Copy files from source bucket to destination
        
        #Unpack and store in destination
        
        
        
        