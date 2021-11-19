
class StagingDataQualitySQL:
    """
    Description: SQL for checking data quality in staging tables.
    """
    
    expected_fields = {
        'yellow_staging': 18,
        'green_staging': 20,
        'fhv_staging': 7,
        'fhvhv_staging': 7
    }
    
    
    check_number_of_fields = ("""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'public'
        AND table_name = '{}'
        ;
    """)
    
    check_number_of_rows = ("""
        SELECT COUNT(*) 
        FROM public.{}
        ;
    """)
    
    get_date_columns = ("""
        SELECT 
        "column" as column_name
        FROM PG_TABLE_DEF pgtd
        WHERE schemaname = 'public'
        AND tablename = '{}'
        AND "column" like '%_datetime'
        ;
    """)
    
    check_null_dates = ("""
        SELECT
            COUNT(*)
        FROM public.{}
        WHERE {} IS NULL
        OR {} IS NULL
        ;
    """)
    
    check_0_passengers = ("""
        SELECT
            COUNT(*)
        FROM public.{}
        WHERE passenger_count = 0
        ;
    """)
    