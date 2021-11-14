
class CreateStagingTablesSQL:
    
    create_yellow_staging = ("""
    CREATE TABLE IF NOT EXISTS public.yellow_staging (
        vendorid varchar(50),
        pickup_datetime varchar(50),
        dropoff_datetime varchar(50),
        passenger_count varchar(50),
        trip_distance varchar(50),
        ratecodeid varchar(50),
        store_and_fwd_flag varchar(50),
        pulocationid varchar(50),
        dolocationid varchar(50),
        payment_type varchar(50),
        fare_amount varchar(50),
        extra varchar(50),
        mta_tax varchar(50),
        tip_amount varchar(50),
        tolls_amount varchar(50),
        improvement_surcharge varchar(50),
        total_amount varchar(50),
        congestion_surcharge varchar(50)
    );
    """)

    create_green_staging  = ("""
    CREATE TABLE IF NOT EXISTS public.green_staging (
        vendorid varchar(50),
        pickup_datetime varchar(50),
        dropoff_datetime varchar(50),
        store_and_fwd_flag varchar(50),
        ratecodeid varchar(50),
        pulocationid varchar(50),
        dolocationid varchar(50),
        passenger_count varchar(50),
        trip_distance varchar(50),
        fare_amount varchar(50),
        extra varchar(50),
        mta_tax varchar(50),
        tip_amount varchar(50),
        tolls_amount varchar(50),
        ehail_fee varchar(50),
        improvement_surcharge varchar(50),
        total_amount varchar(50),
        payment_type varchar(50),
        trip_type varchar(50),
        congestion_surcharge varchar(50)
    );
    """)

    create_fhv_staging = ("""
    CREATE TABLE IF NOT EXISTS public.fhv_staging (
        dispatching_base_num varchar(50),
        pickup_datetime varchar(50),
        dropoff_datetime varchar(50),
        pulocationid varchar(50),
        dolocationid varchar(50),
        sr_flag varchar(50),
        affiliated_base_number varchar(50)
    );
    """)

    create_fhvhv_staging = ("""
    CREATE TABLE IF NOT EXISTS public.fhvhv_staging (
        hvfhs_licencse_num varchar(50),
        dispatching_base_num varchar(50),
        pickup_datetime varchar(50),
        dropoff_datetime varchar(50),
        pulocationid varchar(50),
        dolocationid varchar(50),
        sr_flag varchar(50)
    );
    """)

    create_taxi_zone_lookup_staging = ("""
    CREATE TABLE IF NOT EXISTS public.taxi_zone_lookup_staging (
        geometry GEOMETRY,
        object_id int,
        shape_leng decimal(8,6),
        shape_area decimal(8,6),
        zone varchar(255),
        location_id int,
        borough varchar(255),
        centroid_x decimal(19,11),
        centroid_y decimal(19,11)
    );
    """)
    
    create_taxi_base_lookup_staging = ("""
    CREATE TABLE IF NOT EXISTS public.taxi_base_lookup_staging (
        HighVolumeLicenseNumber varchar(50) NOT NULL,
        LicenseNumber varchar(50) NOT NULL,
        BaseName varchar(50) NOT NULL,
        AppCompanyAffiliation varchar(50) NOT NULL
    );
    """)

    copy_sql = ("""
    COPY public.{}
    FROM '{}'
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    IGNOREHEADER {}
    DELIMITER '{}'
    """)
    
    copy_sql_shape = ("""
    COPY public.{}
    FROM '{}'
    FORMAT SHAPEFILE
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    """
    )

