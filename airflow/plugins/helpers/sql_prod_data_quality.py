
class ProdDataQualitySQL:
    
    check_dim_count = ("""
    SELECT COUNT(*) FROM {}
    ;
    """)