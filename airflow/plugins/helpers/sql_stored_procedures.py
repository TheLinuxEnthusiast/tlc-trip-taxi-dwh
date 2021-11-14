
class StoredProceduresSQL:
    
    replace_nulls = ("""
    CREATE OR REPLACE PROCEDURE replace_nulls(
    tableName text,
    schemaName text
    )
    LANGUAGE plpgsql
    AS $$
      DECLARE
       col RECORD;
       replacement_string VARCHAR(50) := '0';
      BEGIN
        FOR col IN SELECT
                CAST(column_name as VARCHAR) as column_name
              FROM information_schema.columns
              WHERE table_name = tableName 
              AND table_schema = schemaName
        LOOP
          IF (col.column_name = 'vendor_id') THEN
            replacement_string := '0';
          ELSIF (col.column_name = 'passenger_count') THEN
            replacement_string := '1';
          ELSIF (col.column_name = 'ratecodeid') THEN
            replacement_string := '0';
          ELSIF (col.column_name = 'payment_type') THEN
            replacement_string := '0';
          ELSIF (col.column_name = 'store_and_fwd_flag') THEN
            replacement_string := 'N';
          ELSIF (col.column_name = 'ehail_fee') THEN
            replacement_string := '0.0';
          ELSIF (col.column_name = 'trip_type') THEN
            replacement_string := '0';
          ELSIF (col.column_name = 'congestion_surcharge') THEN
            replacement_string := '0.0';
          ELSIF (col.column_name = 'sr_flag') THEN
            replacement_string := '0';
          END IF;

          EXECUTE 'UPDATE '
          + quote_ident(schemaName)
          + '.'
          + quote_ident(tableName)
          + ' SET '
          + quote_ident(col.column_name)
          + ' = ' 
          + quote_literal(replacement_string)
          + ' WHERE '
          + quote_ident(col.column_name) 
          + ' = '
          + quote_literal('');

        END LOOP;
      END;
    $$;
    """)
    
    replace_zero_passenger = ("""
    CREATE OR REPLACE PROCEDURE replace_zero_passenger(
    tableName text,
    schemaName text
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
      EXECUTE 'UPDATE '
          + quote_ident(schemaName)
          + '.'
          + quote_ident(tableName)
          + ' SET passenger_count'
          + ' = '
          + quote_literal('1')
          + ' WHERE passenger_count'
          + ' = '
          + quote_literal('0');
    END;
    $$;
    """)
    
    replace_zero_ratecode = ("""
    CREATE OR REPLACE PROCEDURE replace_zero_ratecode(
    tableName text,
    schemaName text
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
      EXECUTE 'UPDATE '
          + quote_ident(schemaName)
          + '.'
          + quote_ident(tableName)
          + ' SET ratecodeid'
          + ' = '
          + quote_literal('99')
          + ' WHERE ratecodeid'
          + ' = '
          + quote_literal('0');
    END;
    $$;
    """)