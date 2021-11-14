from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
from helpers.sql_stored_procedures import StoredProceduresSQL
#import pandas as pd
#import geopandas as gpd



class CleanStagingData(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 schema="",
                 *args, **kwargs):
        
        super(CleanStagingData, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.schema = schema
    
    
    #def run_sql(redshift_conn, )
    
    def execute(self, context): 
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Replace nulls with zero for all columns
        try:
            self.log.info(f"Cleaning data in {self.table}.....")
            redshift.run("CALL replace_nulls('{}', '{}');".format(self.table, self.schema))
        except Exception as e:
            print(e)
            raise(f"Error cleaning nulls in table {self.table}, exiting.....")
        
        # Replace passenger count 0 with at least 1 as zero passengers does not make sense
        # Only applicable to yellow, green datasets
        if self.table in ["yellow_staging", "green_staging"]:
            try:
                self.log.info(f"Replace passenger count 0 with at least 1")
                redshift.run("CALL replace_zero_passenger('{}', '{}');".format(self.table, self.schema))
            except Exception as e:
                print(e)
                raise(f"Error replacing nulls in {self.table}, exiting.....")
                
         
            # Replace ratecode zeros with 99 which corresponds to unkown
            try:
                self.log.info(f"Replace ratecode zeros with 99")
                redshift.run("CALL replace_zero_ratecode('{}', '{}');".format(self.table, self.schema))
            except Exception as e:
                print(e)
                raise(f"Error replacing 0 in {self.table}, exiting.....")
        
            
            
     
    
        