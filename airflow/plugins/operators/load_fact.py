from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
#from helpers.sql_stored_procedures import StoredProceduresSQL
#from helpers.sql_dimension_tables import CreateDimensionTablesSQL
from helpers.sql_fact_tables import CreateFactTableSQL
from helpers.sql_insert_queries import InsertQueriesSQL



class LoadFact(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 source="",
                 schema="",
                 *args, **kwargs):
        
        super(LoadFact, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.source = source
        self.schema = schema
        
        
    def execute(self, context):
        """
        Description: Loads source data into Fact table (trip_fact)
        
        Arguments:
            context: Metadata from DAG run
            
        Returns:
            None
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Create fact table if it does not already exist
        try:
            self.log.info(f"Creating trip fact table if it does not already exist.......")
            redshift.run(getattr(CreateFactTableSQL, "create_trip_fact"))
        except Exception as e:
            print(e)
            raise(f"Error creating fact table, exiting.....")
        
        # Load data into destination based on source table
        try:
            self.log.info(f"Loading data into fact table.......")
            redshift.run(getattr(InsertQueriesSQL, f"fact_{self.source}_insert"))
        except Exception as e:
            print(e)
            raise(f"Error insertng data, exiting.....")
        
        
            
            