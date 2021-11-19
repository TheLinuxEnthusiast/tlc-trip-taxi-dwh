from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#from helpers.sql_staging_tables import CreateStagingTablesSQL
#from helpers.sql_truncate_staging import TruncateStagingTablesSQL
from helpers.sql_stored_procedures import StoredProceduresSQL
from helpers.sql_functions import FunctionsSQL


class LoadDependencies(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 *args, **kwargs):

        super(LoadDependencies, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
     
    
    def load_dependency(self, redshift_conn, sql_helper):
        """
        Description: Loops through dependant code for DAG run and runs it against the DB
        
        Arguments:
            redshift_conn: Redhsift Connection Object
            sql_helper: Name of class with dependant code
        
        Returns:
            None
        """
        try:
            self.log.info(f"Loading Dependencies for {sql_helper}.....")
            lst = [i for i in dir(sql_helper) if not i.startswith('__')]
            
            for dep in lst:
                redshift_conn.run(getattr(sql_helper, f"{dep}"))
        except Exception as e:
            print(e)
            raise(f"Error loading dependency {sql_helper}.....")
        
    
    def execute(self, context):
        """
        Description: Executes "load_dependency" function
        
        Arguments:
            context: Metadata from DAG run.
            
        Returns:
            None
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.load_dependency(redshift, StoredProceduresSQL)
        self.load_dependency(redshift, FunctionsSQL)
        
        
        
        
    
    