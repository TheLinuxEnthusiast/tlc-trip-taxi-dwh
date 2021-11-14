from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3CopyObjectOperator(BaseOperator):

    template_fields = ('source_bucket_key', 'dest_bucket_key',
                       'source_bucket_name', 'dest_bucket_name')

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

    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=self.aws_credentials_id, verify=self.verify)
        s3_hook.copy_object(self.source_bucket_key, self.dest_bucket_key,
                            self.source_bucket_name, self.dest_bucket_name,
                            self.source_version_id)