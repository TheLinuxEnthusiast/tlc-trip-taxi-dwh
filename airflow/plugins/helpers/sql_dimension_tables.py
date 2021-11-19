
class CreateDimensionTablesSQL:
    """
    Description: DDL SQL statements for Dimension tables.
    """
    create_time_dim = ("""
        CREATE TABLE IF NOT EXISTS public.time_dim (
        event_datetime datetime NOT NULL,
        "hour" int4,
        "day" int4,
        week int4,
        "month" int4,
        "year" int4,
        day_of_week int4,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT time_pkey PRIMARY KEY (event_datetime)
        );  
    """)
    
    
    create_location_dim = ("""
        CREATE TABLE IF NOT EXISTS public.location_dim (
        location_key_id int4 NOT NULL,
        location_id int4 NOT NULL,
        zone varchar(255) NOT NULL,
        borough varchar(255) NOT NULL,
        geometry GEOMETRY NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT location_pkey PRIMARY KEY (location_key_id)
        );
    """)
    
    
    create_vendor_dim = ("""
     CREATE TABLE IF NOT EXISTS public.vendor_dim (
        vendor_key_id int4 NOT NULL, 
        vendor_id int4 NOT NULL,
        vendor_description varchar(255) NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT vendor_pkey PRIMARY KEY (vendor_key_id)
     );
    """)
    

    create_trip_type_dim = ("""
    CREATE TABLE IF NOT EXISTS public.trip_type_dim (
        trip_type_key_id int4 NOT NULL,
        trip_type_id int4 NOT NULL,
        trip_type_description varchar(255) NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT trip_type_pkey PRIMARY KEY (trip_type_key_id)
    );
    """)
    
    
    create_ratecode_dim = ("""
    CREATE TABLE IF NOT EXISTS public.ratecode_dim (
        ratecode_key_id int4 NOT NULL,
        ratecode_id int4 NOT NULL,
        ratecode_description varchar(255) NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT ratecode_pkey PRIMARY KEY (ratecode_key_id)
    );
    """)
    
    
    create_taxi_base_dim = ("""
    CREATE TABLE IF NOT EXISTS public.taxi_base_dim (
        taxi_base_key_id varchar(255) NOT NULL, --license_number
        taxi_base_description varchar(255) NOT NULL,
        -- license_number varchar(255) NOT NULL,
        high_volume_license_number varchar(255),
        base_name varchar(255) NOT NULL,
        app_company_affiliation varchar(255) NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT taxi_base_pkey PRIMARY KEY (taxi_base_key_id)
    );
    """)
    
    
    create_payment_type_dim = ("""
    CREATE TABLE IF NOT EXISTS public.payment_type_dim (
        payment_type_key_id int4 NOT NULL,
        payment_type_id int4 NOT NULL,
        payment_type_description varchar(255) NOT NULL,
        insertion_datetime datetime NOT NULL,
        CONSTRAINT payment_type_pkey PRIMARY KEY (payment_type_key_id)
     );
    """)
    
    