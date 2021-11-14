from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
from helpers.sql_staging_data_quality import StagingDataQualitySQL

class StagingDataQuality(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 *args,
                 **kwargs):
        
        super(StagingDataQuality, self).__init__(*args, **kwargs)
        self.table = table
        self.aws_credentials_id = aws_credentials_id
        self.redshift_conn_id=redshift_conn_id

    
    def execute(self, context):
        
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        expected = StagingDataQualitySQL.expected_fields
        
        try:
            self.log.info(f"Performing data quality checks for {self.table}.....")
            conn = redshift.get_conn()
            cursor = conn.cursor()
            cursor.execute(StagingDataQualitySQL.check_number_of_fields.format(self.table))
            #redshift.run(StagingDataQualitySQL.check_number_of_fields.format(self.table))
            sources = cursor.fetchall()
            self.log.info(f"{sources}")
            
            if sources[0][0] != expected[f'{self.table}']:
                raise("Number of fields differs from what is expected")
                
            #row_check = redshift.run(StagingDataQualitySQL.check_number_of_rows.format(self.table))
            cursor.execute(StagingDataQualitySQL.check_number_of_rows.format(self.table))
            sources = cursor.fetchall()
            self.log.info(f"{sources}")
            
            if sources[0][0] > 0:
                pass
            else:
                raise("Number of rows is less than expected")
                
            
        except Exception as e:
            print(e)
            raise(f"Error during data quality checks on {self.table}, exiting.....")
        
        
        
    
        