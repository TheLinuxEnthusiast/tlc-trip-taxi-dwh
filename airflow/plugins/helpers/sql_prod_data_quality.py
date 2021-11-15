
class ProdDataQualitySQL:
    
    check_dim_count = ("""
    SELECT COUNT(*) FROM {}
    ;
    """)
    
    check_fact_rows = ("""
    SELECT 
        count(*)
    FROM public.trip_fact
    WHERE TRUNC(insertion_datetime) = CURRENT_DATE
    AND taxi_base_key_id = 'GN0001'
    """)