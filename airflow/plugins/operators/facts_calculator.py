import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class FactsCalculatorOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 origin_table="",
                 destination_table="",
                 fact_column="",
                 groupby_column="",
                 *args, **kwargs):

        super(FactsCalculatorOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id=redshift_conn_id
        self.origin_table=origin_table
        self.destination_table=destination_table
        self.fact_column=fact_column
        self.groupby_column=groupby_column

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        facts_sql_template = f"""
            DROP TABLE IF EXISTS {self.destination_table};
            CREATE TABLE {self.destination_table} AS
            SELECT
                {self.groupby_column},
                MAX({self.fact_column}) AS max_{self.fact_column},
                MIN({self.fact_column}) AS min_{self.fact_column},
                AVG({self.fact_column}) AS average_{self.fact_column}
            FROM {self.origin_table}
            GROUP BY {self.groupby_column};
            """
        
        redshift_hook.run(facts_sql_template)
        
        
