
class CreateFactTableSQL:
    
    create_trip_fact = ("""
     CREATE TABLE IF NOT EXISTS public.trip_fact (
        trip_key_id bigint IDENTITY(1,1) NOT NULL,
        taxi_base_key_id varchar(50) NOT NULL,
        vendor_key_id int4 NOT NULL,
        pickup_datetime datetime NOT NULL,
        dropoff_datetime datetime NOT NULL,
        pu_location_key_id int4 NOT NULL,
        do_location_key_id int4 NOT NULL,
        passenger_count int4,
        ratecode_key_id int4 NOT NULL,
        trip_duration decimal(19,11),
        trip_distance decimal(19,11),
        store_and_fwd_flag int4,
        payment_type_key_id int4 NOT NULL,
        fare_amount decimal(19,11),
        extra decimal(19,11),
        mta_tax decimal(19,11),
        tip_amount decimal(19,11),
        tolls_amount decimal(19,11),
        improvement_surcharge decimal(19,11),
        total_amount decimal(19,11),
        congestion_surcharge decimal(19,11),
        ehail_fee decimal(19,11),
        trip_type_key_id int4 NOT NULL,
        -- sr_flag ??
        CONSTRAINT trip_pkey PRIMARY KEY (trip_key_id),
        FOREIGN KEY(taxi_base_key_id) REFERENCES public.taxi_base_dim(taxi_base_key_id),
        FOREIGN KEY(vendor_key_id) REFERENCES public.vendor_dim(vendor_key_id),
        FOREIGN KEY(pickup_datetime) REFERENCES public.time_dim(event_datetime),
        FOREIGN KEY(dropoff_datetime) REFERENCES public.time_dim(event_datetime),
        FOREIGN KEY(pu_location_key_id) REFERENCES public.location_dim(location_key_id),
        FOREIGN KEY(do_location_key_id) REFERENCES public.location_dim(location_key_id),
        FOREIGN KEY(ratecode_key_id) REFERENCES public.ratecode_dim(ratecode_key_id),
        FOREIGN KEY(payment_type_key_id) REFERENCES public.payment_type_dim(payment_type_key_id),
        FOREIGN KEY(trip_type_key_id) REFERENCES public.trip_type_dim(trip_type_key_id)
        );
    """)