
class InsertQueriesSQL:
    
    time_dim_insert = ("""
        CREATE TEMP TABLE IF NOT EXISTS time_temp (LIKE public.time_dim);

        INSERT INTO time_temp (
        event_datetime,
        hour,
        day,
        week,
        month,
        year,
        day_of_week
        )
        SELECT DISTINCT
                       x.event_datetime,
                       x.hour,
                       x.day,
                       x.week,
                       x.month,
                       x.year,
                       x.day_of_week
                FROM (
                    SELECT
                        CAST({} as datetime) as event_datetime,
                        extract(hour from event_datetime) as hour, 
                        extract(day from event_datetime) as day,
                        extract(week from event_datetime) as week, 
                        extract(month from event_datetime) as month, 
                        extract(year from event_datetime) as year, 
                        extract(dayofweek from event_datetime) as day_of_week
                    FROM {} s1
                    UNION
                        SELECT
                        CAST({} as datetime) as event_datetime,
                        extract(hour from event_datetime) as hour, 
                        extract(day from event_datetime) as day,
                        extract(week from event_datetime) as week, 
                        extract(month from event_datetime) as month, 
                        extract(year from event_datetime) as year, 
                        extract(dayofweek from event_datetime) as day_of_week
                    FROM {} s2
                  ) x;
        
        BEGIN TRANSACTION;
        
        DELETE FROM public.time_dim
        USING time_temp
        WHERE public.time_dim.event_datetime = time_temp.event_datetime;

        INSERT INTO public.time_dim (
              event_datetime,
              hour,
              day,
              week,
              month,
              year,
              day_of_week
              )
          SELECT 
            event_datetime,
            hour,
            day,
            week,
            month,
            year,
            day_of_week
          FROM time_temp;
    
        END TRANSACTION;
        
        DROP TABLE IF EXISTS time_temp;
    """)
    
    
    location_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS location_temp (like public.location_dim);

    INSERT INTO location_temp(
        location_key_id,
        location_id,
        borough,
        zone,
        geometry
        )
        SELECT 
                ROW_NUMBER() OVER() as location_key_id,  
                location_id,
                borough,
                zone,
                geometry
       FROM taxi_zone_lookup_staging;

    BEGIN TRANSACTION;

    DELETE FROM public.location_dim
    USING location_temp
    WHERE public.location_dim.location_id = location_temp.location_id;


    INSERT INTO public.location_dim (
        location_key_id,
        location_id,
        borough,
        zone,
        geometry
        )
        SELECT
          location_key_id,
          location_id,
          borough,
          zone,
          geometry
        FROM location_temp;


    END TRANSACTION;

    DROP TABLE IF EXISTS location_temp;
    """)
    
    vendor_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS vendor_temp (
    vendor_key_id int4 NOT NULL,
    vendor_id int4 NOT NULL,
    vendor_description varchar(255) NOT NULL
    );

    INSERT INTO vendor_temp (
        vendor_key_id,
        vendor_id,
        vendor_description
        )
    SELECT
        ROW_NUMBER() OVER() as vendor_key_id,
        CAST(s.vendor_id as int4) as vendor_id,
        CASE 
            WHEN s.vendor_id = 1 THEN 'Creative Mobile Technologies LLC'
            WHEN s.vendor_id = 2 THEN 'VeriFone Inc'
            ELSE 'Unknown' END AS vendor_description
        FROM (
            SELECT CAST('1' as int4) as vendor_id
              UNION
            SELECT CAST('2' as int4) as vendor_id
              UNION
            SELECT CAST('0' as int4) as vendor_id
        ) s;

    BEGIN TRANSACTION;

    DELETE FROM public.vendor_dim
    USING vendor_temp
    WHERE public.vendor_dim.vendor_id = vendor_temp.vendor_id;

    INSERT INTO public.vendor_dim (
        vendor_key_id,
        vendor_id,
        vendor_description
        )
        SELECT
        vendor_key_id,
        vendor_id,
        vendor_description
        FROM vendor_temp;


    END TRANSACTION;

    DROP TABLE IF EXISTS vendor_temp;
    """)
    
    
    ratecode_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS ratecode_temp (like public.ratecode_dim);

    INSERT INTO ratecode_temp (
        ratecode_key_id,
        ratecode_id,
        ratecode_description
        )
        SELECT
        ROW_NUMBER() OVER() as ratecode_key_id,
        s.ratecode_id,
        CASE
            WHEN s.ratecode_id = 1 THEN 'Standard rate'
            WHEN s.ratecode_id = 2 THEN 'JFK'
            WHEN s.ratecode_id = 3 THEN 'Newark'
            WHEN s.ratecode_id = 4 THEN 'Nassau or Westchester'
            WHEN s.ratecode_id = 5 THEN 'Negotiated fare'
            WHEN s.ratecode_id = 6 THEN 'Group ride'
            WHEN s.ratecode_id = 99 THEN 'Unknown'
            END AS ratecode_description
        FROM (
          SELECT CAST('1' as int4) as ratecode_id
              UNION
            SELECT CAST('2' as int4) as ratecode_id
              UNION
            SELECT CAST('3' as int4) as ratecode_id
             UNION
            SELECT CAST('4' as int4) as ratecode_id
             UNION
            SELECT CAST('5' as int4) as ratecode_id
             UNION
            SELECT CAST('6' as int4) as ratecode_id
             UNION
            SELECT CAST('99' as int4) as ratecode_id
        ) s;

    BEGIN TRANSACTION;

    DELETE FROM public.ratecode_dim
    USING ratecode_temp
    WHERE public.ratecode_dim.ratecode_id = ratecode_temp.ratecode_id;


    INSERT INTO public.ratecode_dim (
        ratecode_key_id,
        ratecode_id,
        ratecode_description
        )
      SELECT
      ratecode_key_id,
      ratecode_id,
      ratecode_description
      FROM ratecode_temp;


    END TRANSACTION;

    DROP TABLE IF EXISTS ratecode_temp;
    """)
    
    
    payment_type_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS payment_type_temp (like public.payment_type_dim);

    INSERT INTO payment_type_temp(
        payment_type_key_id,
        payment_type_id,
        payment_type_description
        )
        SELECT
            ROW_NUMBER() OVER() as payment_type_key_id,
            payment_type_id,
            CASE
                WHEN s.payment_type_id = 1 THEN 'Credit Card'
                WHEN s.payment_type_id = 2 THEN 'Cash'
                WHEN s.payment_type_id = 3 THEN 'No charge'
                WHEN s.payment_type_id = 4 THEN 'Dispute'
                WHEN s.payment_type_id = 5 THEN 'Unknown'
                WHEN s.payment_type_id = 6 THEN 'Voided trip'
                ELSE 'Unknown' END AS payment_type_description
         FROM (
        SELECT CAST('1' as int4) as payment_type_id
          UNION
        SELECT CAST('2' as int4) as payment_type_id
          UNION
        SELECT CAST('3' as int4) as payment_type_id
         UNION
        SELECT CAST('4' as int4) as payment_type_id
         UNION
        SELECT CAST('5' as int4) as payment_type_id
         UNION
        SELECT CAST('6' as int4) as payment_type_id
         UNION
        SELECT CAST('0' as int4) as payment_type_id
        ) s;

    BEGIN TRANSACTION;

    DELETE FROM public.payment_type_dim
    USING payment_type_temp
    WHERE public.payment_type_dim.payment_type_id = payment_type_temp.payment_type_id;


    INSERT INTO public.payment_type_dim (
        payment_type_key_id,
        payment_type_id,
        payment_type_description
        )
      SELECT
        payment_type_key_id,
        payment_type_id,
        payment_type_description
      FROM payment_type_temp;


    END TRANSACTION;

    DROP TABLE IF EXISTS payment_type_temp;
    """)
    
    
    fhv_taxi_base_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS taxi_base_temp (like public.taxi_base_dim);
    
    INSERT INTO taxi_base_temp(
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        )
        SELECT
              fs.taxi_base_key_id,
              'FHV taxi Base' AS taxi_base_description,
              NULL AS high_volume_license_number,
              'None' as base_name,
              'Uber or Lyft' AS app_company_affiliation
              FROM (
                SELECT DISTINCT
                  dispatching_base_num as taxi_base_key_id
                  FROM fhv_staging
              ) fs;
              
    BEGIN TRANSACTION;

    DELETE FROM public.taxi_base_dim
    USING taxi_base_temp
    WHERE public.taxi_base_dim.taxi_base_key_id = taxi_base_temp.taxi_base_key_id;
    
    INSERT INTO public.taxi_base_dim(
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        )
        SELECT
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        FROM taxi_base_temp;

    END TRANSACTION;

    DROP TABLE IF EXISTS taxi_base_temp;
    """)
    
    
    taxi_base_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS taxi_base_temp (like public.taxi_base_dim);

    INSERT INTO taxi_base_temp(
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        )
        SELECT
          licensenumber as taxi_base_key_id,
          'FHV_HV taxi Base' AS taxi_base_description,
          highvolumelicensenumber AS high_volume_license_number,
          basename AS base_name,
          appcompanyaffiliation AS app_company_affiliation
        FROM taxi_base_lookup_staging

          UNION

          SELECT
             'YW0001' AS taxi_base_key_id,
             'Yellow Taxi Base' AS taxi_base_description,
             NULL AS high_volume_license_number,
             'None' AS base_name,
             'Curb or Arro' AS app_company_affiliation

           UNION

           SELECT
             'GN0001' AS taxi_base_key_id,
             'Green Taxi Base' AS taxi_base_description,
             NULL AS high_volume_license_number,
             'None' AS base_name,
             'Curb or Arro' AS app_company_affiliation;

    BEGIN TRANSACTION;

    DELETE FROM public.taxi_base_dim
    USING taxi_base_temp
    WHERE public.taxi_base_dim.taxi_base_key_id = taxi_base_temp.taxi_base_key_id;


    INSERT INTO public.taxi_base_dim(
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        )
        SELECT
        taxi_base_key_id,
        taxi_base_description,
        high_volume_license_number,
        base_name, 
        app_company_affiliation
        FROM taxi_base_temp;


    END TRANSACTION;

    DROP TABLE IF EXISTS taxi_base_temp;
    """)
    
    
    trip_type_dim_insert = ("""
    CREATE TEMP TABLE IF NOT EXISTS trip_type_temp (like public.trip_type_dim);

    INSERT INTO trip_type_temp (
        trip_type_key_id,
        trip_type_id,
        trip_type_description
        )
        SELECT 
            ROW_NUMBER() OVER() as trip_type_key_id,
             s.trip_type_id,
             CASE
                  WHEN s.trip_type_id = 1 THEN 'Street Hail'
                  WHEN s.trip_type_id = 2 THEN 'Dispatch'
                  WHEN s.trip_type_id = 0 THEN 'Unknown'
                  END as trip_type_description
        FROM (
          SELECT
             CAST('1' as int4) as trip_type_id
             UNION
          SELECT
             CAST('2' as int4) as trip_type_id
             UNION
          SELECT
             CAST('0' as int4) as trip_type_id
        ) s;

    BEGIN TRANSACTION;

    DELETE FROM public.trip_type_dim
    USING trip_type_temp
    WHERE public.trip_type_dim.trip_type_id = trip_type_temp.trip_type_id;


    INSERT INTO public.trip_type_dim (
        trip_type_key_id,
        trip_type_id,
        trip_type_description
        )
      SELECT
        trip_type_key_id,
        trip_type_id,
        trip_type_description
      FROM trip_type_temp;

    END TRANSACTION;

    DROP TABLE IF EXISTS trip_type_temp;
    """)
    
    
    fact_yellow_insert = ("""
    INSERT INTO public.trip_fact (
    taxi_base_key_id,
    vendor_key_id,
    pickup_datetime,
    dropoff_datetime,
    pu_location_key_id,
    do_location_key_id,
    passenger_count,
    ratecode_key_id,
    trip_distance,
    store_and_fwd_flag,
    payment_type_key_id,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    ehail_fee,
    trip_type_key_id
    )
    SELECT
      'YW0001' as taxi_base_key_id,
      vd.vendor_key_id,
      CAST(ys.pickup_datetime as datetime) as pickup_datetime,
      CAST(ys.dropoff_datetime as datetime) as dropoff_datetime,
      ld_pu.location_key_id,
      ld_do.location_key_id,
      CAST(passenger_count as int4) as passenger_count,
      rcd.ratecode_key_id,
      CAST(trip_distance as decimal(19,11)) as trip_distance,
      CASE 
        WHEN store_and_fwd_flag = 'N' THEN CAST('0' as int4)
        WHEN store_and_fwd_flag = 'Y' THEN CAST('1' as int4)
        END as store_and_fwd_flag,
      ptd.payment_type_key_id,
      CAST(fare_amount as decimal(19,11)) as fare_amount,
      CAST(extra as decimal(19,11)) as extra,
      CAST(mta_tax as decimal(19,11)) as mta_tax,
      CAST(tip_amount as decimal(19,11)) as tip_amount,
      CAST(tolls_amount as decimal(19,11)) as tolls_amount,
      CAST(improvement_surcharge as decimal(19,11)) as improvement_surcharge,
      CAST(total_amount as decimal(19,11)) as total_amount,
      CAST(congestion_surcharge as decimal(19,11)) as congestion_surcharge,
      CAST('0.0' as decimal(19,11)) as ehail_fee,
      CAST('1' as int4) as trip_type_key_id
    FROM yellow_staging ys
    JOIN vendor_dim vd
    ON vd.vendor_id = ys.vendorid
    JOIN location_dim ld_pu
    ON ld_pu.location_id = ys.pulocationid
    JOIN location_dim ld_do
    ON ld_do.location_id = ys.dolocationid
    JOIN ratecode_dim rcd
    ON rcd.ratecode_id = ys.ratecodeid
    JOIN payment_type_dim ptd
    ON ptd.payment_type_id = payment_type;
    """)
    
    
    fact_green_insert = ("""
    INSERT INTO public.trip_fact (
    taxi_base_key_id,
    vendor_key_id,
    pickup_datetime,
    dropoff_datetime,
    pu_location_key_id,
    do_location_key_id,
    passenger_count,
    ratecode_key_id,
    trip_distance,
    store_and_fwd_flag,
    payment_type_key_id,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    ehail_fee,
    trip_type_key_id
    )
    SELECT
      'GN0001' as taxi_base_key_id,
      vd.vendor_key_id,
      CAST(gs.pickup_datetime as datetime) as pickup_datetime,
      CAST(gs.dropoff_datetime as datetime) as dropoff_datetime,
      ld_pu.location_key_id,
      ld_do.location_key_id,
      CAST(passenger_count as int4) as passenger_count,
      rcd.ratecode_key_id,
      CAST(trip_distance as decimal(19,11)) as trip_distance,
      CASE 
        WHEN store_and_fwd_flag = 'N' THEN CAST('0' as int4)
        WHEN store_and_fwd_flag = 'Y' THEN CAST('1' as int4)
        END as store_and_fwd_flag,
      ptd.payment_type_key_id,
      CAST(fare_amount as decimal(19,11)) as fare_amount,
      CAST(extra as decimal(19,11)) as extra,
      CAST(mta_tax as decimal(19,11)) as mta_tax,
      CAST(tip_amount as decimal(19,11)) as tip_amount,
      CAST(tolls_amount as decimal(19,11)) as tolls_amount,
      CAST(improvement_surcharge as decimal(19,11)) as improvement_surcharge,
      CAST(total_amount as decimal(19,11)) as total_amount,
      CAST(congestion_surcharge as decimal(19,11)) as congestion_surcharge,
      CAST(ehail_fee as decimal(19,11)) as ehail_fee,
      ttd.trip_type_key_id
    FROM green_staging gs
    JOIN vendor_dim vd
    ON vd.vendor_id = gs.vendorid
    JOIN location_dim ld_pu
    ON ld_pu.location_id = gs.pulocationid
    JOIN location_dim ld_do
    ON ld_do.location_id = gs.dolocationid
    JOIN ratecode_dim rcd
    ON rcd.ratecode_id = gs.ratecodeid
    JOIN payment_type_dim ptd
    ON ptd.payment_type_id = gs.payment_type
    JOIN trip_type_dim ttd
    ON ttd.trip_type_id = gs.trip_type;
    """)
    
    
    fact_fhv_insert = ("""
    INSERT INTO public.trip_fact (
    taxi_base_key_id,
    vendor_key_id,
    pickup_datetime,
    dropoff_datetime,
    pu_location_key_id,
    do_location_key_id,
    passenger_count,
    ratecode_key_id,
    trip_distance,
    store_and_fwd_flag,
    payment_type_key_id,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    ehail_fee,
    trip_type_key_id
    )
    SELECT
      tbd.taxi_base_key_id,
      CAST('0' as int4) as vendor_key_id,
      CAST(fs.pickup_datetime as datetime) as pickup_datetime,
      CAST(fs.dropoff_datetime as datetime) as dropoff_datetime,
      ld_pu.location_key_id,
      ld_do.location_key_id,
      CASE
            WHEN sr_flag = '1' THEN CAST('2' as int4) 
            WHEN sr_flag = '0' THEN CAST('1' as int4)
            END as passenger_count,
      CAST('1' as int4) as ratecode_key_id,
      CAST(haversine(tzls_pu.centroid_y, 
                     tzls_pu.centroid_x, 
                     tzls_do.centroid_y, 
                     tzls_do.centroid_x) as decimal(19,11)) as trip_distance,
      CAST('0' as int4) as store_and_fwd_flag,
      CAST('1' as int4) as payment_type_key_id,
      CAST(estimate_fair(trip_distance, 
                         calculate_duration(pickup_datetime, dropoff_datetime)
                         ) as decimal(19,11)) as fare_amount,
      CAST('0.0' as decimal(19,11)) as extra,
      CAST('0.0' as decimal(19,11)) as mta_tax,
      CAST('0.0' as decimal(19,11)) as tip_amount,
      CAST('0.0' as decimal(19,11)) as tolls_amount,
      CAST('0.0' as decimal(19,11)) as improvement_surcharge,
      CAST(fare_amount as decimal(19,11)) as total_amount,
      CAST('0.0' as decimal(19,11)) as congestion_surcharge,
      CAST('0.0' as decimal(19,11)) as ehail_fee,
      CAST('2' as int4) as trip_type_key_id
    FROM fhv_staging fs
    JOIN taxi_zone_lookup_staging tzls_pu
    ON tzls_pu.location_id = fs.pulocationid
    JOIN taxi_zone_lookup_staging tzls_do
    ON tzls_do.location_id = fs.dolocationid
    JOIN location_dim ld_pu
    ON ld_pu.location_id = fs.pulocationid
    JOIN location_dim ld_do
    ON ld_do.location_id = fs.dolocationid
    JOIN taxi_base_dim tbd
    ON tbd.taxi_base_key_id = fs.dispatching_base_num;
    """)
    
    fact_fhvhv_insert = ("""
    INSERT INTO public.trip_fact (
    taxi_base_key_id,
    vendor_key_id,
    pickup_datetime,
    dropoff_datetime,
    pu_location_key_id,
    do_location_key_id,
    passenger_count,
    ratecode_key_id,
    trip_distance,
    store_and_fwd_flag,
    payment_type_key_id,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    ehail_fee,
    trip_type_key_id
    )
    SELECT
      tbd.taxi_base_key_id,
      CAST('0' as int4) as vendor_key_id,
      CAST(fs.pickup_datetime as datetime) as pickup_datetime,
      CAST(fs.dropoff_datetime as datetime) as dropoff_datetime,
      ld_pu.location_key_id,
      ld_do.location_key_id,
      CASE
            WHEN sr_flag = '1' THEN CAST('2' as int4) 
            WHEN sr_flag = '0' THEN CAST('1' as int4)
            END as passenger_count,
      CAST('1' as int4) as ratecode_key_id,
      CAST(haversine(tzls_pu.centroid_y, 
                     tzls_pu.centroid_x, 
                     tzls_do.centroid_y, 
                     tzls_do.centroid_x) as decimal(19,11)) as trip_distance,
      CAST('0' as int4) as store_and_fwd_flag,
      CAST('1' as int4) as payment_type_key_id,
      CAST(estimate_fair(trip_distance, 
                         calculate_duration(pickup_datetime, dropoff_datetime)
                         ) as decimal(19,11)) as fare_amount,
      CAST('0.0' as decimal(19,11)) as extra,
      CAST('0.0' as decimal(19,11)) as mta_tax,
      CAST('0.0' as decimal(19,11)) as tip_amount,
      CAST('0.0' as decimal(19,11)) as tolls_amount,
      CAST('0.0' as decimal(19,11)) as improvement_surcharge,
      CAST(fare_amount as decimal(19,11)) as total_amount,
      CAST('0.0' as decimal(19,11)) as congestion_surcharge,
      CAST('0.0' as decimal(19,11)) as ehail_fee,
      CAST('2' as int4) as trip_type_key_id
    FROM fhvhv_staging fs
    JOIN taxi_zone_lookup_staging tzls_pu
    ON tzls_pu.location_id = fs.pulocationid
    JOIN taxi_zone_lookup_staging tzls_do
    ON tzls_do.location_id = fs.dolocationid
    JOIN location_dim ld_pu
    ON ld_pu.location_id = fs.pulocationid
    JOIN location_dim ld_do
    ON ld_do.location_id = fs.dolocationid
    JOIN taxi_base_dim tbd
    ON tbd.taxi_base_key_id = fs.dispatching_base_num;
    """)
    
    
    