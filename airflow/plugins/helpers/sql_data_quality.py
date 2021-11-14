
class FixDataQualitySQL:
    
    replace_null_vendor_id = ("""
    UPDATE {}
    SET vendor_id = '0'
    WHERE vendor_id = '';
    """)
    
    replace_0_passenger_id = ("""
    BEGIN;
    UPDATE {}
    SET passenger_count = 1
    WHERE passenger_count = 0
    """)
    
    replace_null_ratecode_id = ("""
    UPDATE {}
    SET ratecodeid = '99'
    WHERE ratecodeid = '';
    """)
    
    replace_null_payment_type = ("""
    UPDATE {}
    SET payment_type = '0'
    WHERE payment_type = '';
    """)
    
    replace_null_trip_type = ("""
    UPDATE {}
    SET trip_type = '0'
    WHERE trip_type = '';
    """)