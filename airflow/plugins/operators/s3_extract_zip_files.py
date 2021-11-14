from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import gzip
import boto3


class S3ExtractZipFiles(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            source_bucket_key,
            dest_bucket_key,
            source_bucket_name=None,
            dest_bucket_name=None,
            source_version_id=None,
            aws_credentials_id='aws_default',
            verify=None,
            *args, **kwargs):
        super(S3CopyObjectOperator, self).__init__(*args, **kwargs)

        self.source_bucket_key = source_bucket_key
        self.dest_bucket_key = dest_bucket_key
        self.source_bucket_name = source_bucket_name
        self.dest_bucket_name = dest_bucket_name
        self.source_version_id = source_version_id
        self.aws_credentials_id = aws_credentials_id
        self.verify = verify

        
    def copy_file_to_s3(self, s3_hook):
        rendered_key = self.dest_bucket_key.format(**context)
        s3_path_destination = "s3://{}/{}".format(self.dest_bucket_name, rendered_key)
        
        
    
    
    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=self.aws_credentials_id, verify=self.verify)
        conn = s3_hook.get_conn()
        
        #Check if key exists in source bucket
        try:
            if s3_hook.check_for_key(self.source_bucket_key, bucket_name=self.source_bucket_name):
                #Fetch file
                object_ = s3_hook.get_key(self.source_bucket_key, bucket_name=self.source_bucket_name)
                
                file_obj = gzip.GzipFile(object_['Body'].read())
                
                
            else:
                raise("Unable to find taxi zone files")
                
            #If exists, extract zip files into destination bucket
            
            
        except Exception as e:
            print(e)
            raise()