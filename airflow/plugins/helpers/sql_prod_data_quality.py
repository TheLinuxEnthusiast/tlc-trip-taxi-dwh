
class ProdDataQualitySQL:
    
    check_dim_count = ("""
    SELECT COUNT(*) FROM {}
    ;
    """)
    
    check_fact_count = ("""
    SELECT 
        count(*)
    FROM public.trip_fact tf
    JOIN public.taxi_base_dim tbd
    ON tbd.taxi_base_key_id = tf.taxi_base_key_id
    WHERE TRUNC(tf.insertion_datetime) = CURRENT_DATE
    AND tf.taxi_base_key_id in (select distinct taxi_base_key_id 
                                from public.taxi_base_dim
                                where taxi_base_description = '{}');
    """)