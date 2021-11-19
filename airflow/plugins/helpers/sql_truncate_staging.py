
class TruncateStagingTablesSQL:
    """
    Description: SQL for truncating tables.
    """
    TRUNCATE_STAGING = ("""
    DELETE FROM public.{}
    ;
    """)