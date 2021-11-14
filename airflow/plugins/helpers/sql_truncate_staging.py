
class TruncateStagingTablesSQL:
    
    TRUNCATE_STAGING = ("""
    DELETE FROM public.{}
    ;
    """)