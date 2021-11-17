from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
#from helpers.sql_staging_data_quality import StagingDataQualitySQL
from helpers.sql_prod_data_quality import ProdDataQualitySQL

class ProdDataQualityCheck(BaseOperator):
    
    dims = {
        "time": 0,
        "location": 263,
        "vendor": 3,
        "ratecode": 7,
        "payment_type": 7,
        "taxi_base": [40, 617],
        "trip_type": 3
    }
    
    taxi_base_ref = {
        "yellow": "Yellow",
        "green": "Green",
        "fhv": "FHV",
        "fhvhv": "FHV_HV"
    }
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 source="",
                 *args,
                 **kwargs):
        
        super(ProdDataQualityCheck, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.redshift_conn_id=redshift_conn_id
        self.source = source
        
        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Check Number of rows in dimensions is not zero
        try:
            self.log.info(f"Checking dimensions for accurate row counts.....")
            conn = redshift.get_conn()
            cursor = conn.cursor()
            
            for key, value in ProdDataQualityCheck.dims.items():
                sql_formatted = ProdDataQualitySQL.check_dim_count.format(f"public.{key}_dim")
                cursor.execute(sql_formatted)
                result = cursor.fetchall()
                self.log.info(f"{result}")
                
                if key == "time":
                    if result[0][0] > 0:
                        pass
                    else:
                        raise(f"Issue with number of rows in {key} dimension")
                elif key == "taxi_base":
                    if result[0][0] in value:
                        pass
                    else:
                        raise(f"Issue with number of rows in {key} dimension")
                elif result[0][0] != value:
                    raise(f"Issue with number of rows in {key} dimension")

        except Exception as e:
            print(e)
            raise("Issues checking row count")

    
        # Check if rows were inserted into fact
        try:
            sql_formatted = ProdDataQualitySQL.check_fact_count.format(f"{ProdDataQualityCheck.taxi_base_ref[self.source]}")
            cursor.execute(sql_formatted)
            result = cursor.fetchall()
            self.log.info(f"{result}")
            
            if result[0][0] > 0:
                pass
            else:
                raise(f"Issue with number of rows in trip fact for source {self.source}")
            
            
        except Exception as e:
            print(e)
            raise("Issues checking row count")
    
        