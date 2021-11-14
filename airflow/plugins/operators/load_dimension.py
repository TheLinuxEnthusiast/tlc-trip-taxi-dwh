from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
#from helpers.sql_stored_procedures import StoredProceduresSQL
from helpers.sql_dimension_tables import CreateDimensionTablesSQL
from helpers.sql_insert_queries import InsertQueriesSQL


class LoadDimension(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 source="",
                 destination="",
                 schema="",
                 *args, **kwargs):
        
        super(LoadDimension, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.source = source
        self.destination = destination
        self.schema = schema
        
        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Create dimension table if it does not already exist
        try:
            self.log.info(f"Creating {self.destination} dimension if it does not exist")
            redshift.run(getattr(CreateDimensionTablesSQL, f"create_{self.destination}_dim"))
        except Exception as e:
            print(e)
            raise(f"Error creating {self.destination} dimension, exiting.....")
            
        # Execute insert SQL statements
        try:
            self.log.info(f"Inserting into {self.destination} dimension.....")
            type_ = f"{self.destination}_dim_insert"
            sql_insert_statement = getattr(InsertQueriesSQL, f"{type_}")
            if self.destination == "time":
                # prefix = LoadDimension.date_col_prefix[f"{self.source}"]
                sql_formatted = sql_insert_statement.format(f"pickup_datetime",
                                                            f"{self.source}_staging",
                                                            f"dropoff_datetime",
                                                            f"{self.source}_staging")
            else:
                sql_formatted = sql_insert_statement
                
            if self.source == 'fhv' and self.destination == 'taxi_base':
                sql_insert_statement_2 = getattr(InsertQueriesSQL, f"{self.source}_{type_}")
                redshift.run(sql_insert_statement_2)
                
            
            redshift.run(sql_formatted)
            
        except Exception as e:
            print(e)
            raise(f"Error creating {self.table}, exiting.....")
            
        
        