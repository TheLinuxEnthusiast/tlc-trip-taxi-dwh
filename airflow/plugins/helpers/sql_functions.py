
class FunctionsSQL:
    
    haversine_distance_function = ("""
    CREATE OR REPLACE FUNCTION haversine(x_pickup decimal(19,11),
                                     y_pickup decimal(19,11),
                                     x_dropoff decimal(19,11),
                                     y_dropoff decimal(19,11))
                                     returns decimal(19,11)
                                     stable
                                     as $$
                                     
                                     import math
                                     R = 3963.0
                                     lat1 = math.radians(x_pickup)
                                     lon1 = math.radians(y_pickup)
                                     lat2 = math.radians(x_dropoff)
                                     lon2 = math.radians(y_dropoff)
                                     
                                     dlon = lon2 - lon1
                                     dlat = lat2 - lat1
                                     a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
                                     
                                     #c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                                     c = 2*math.asin(math.sqrt(a))
                                     
                                     distance = R * c
                                     return distance
                                     
                                     $$ language plpythonu;
    """)
    
    calculate_duration_function = ("""
    CREATE OR REPLACE FUNCTION calculate_duration(start_datetime varchar(50),
                                                  end_datetime varchar(50))
                                                  returns decimal(19,11)
                                                  stable
                                                  as $$
                                                  
                                                  from datetime import datetime
                                                  start1 = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
                                                  end1 = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")
                                                  
                                                  delta = end1 - start1
                                                  
                                                  journey_time = delta.seconds / 60.0
                                                  return journey_time
                                                  
                                                  $$ language plpythonu;
    """)
    
    estimate_fair_function = ("""
    CREATE OR REPLACE FUNCTION estimate_fair(distance decimal(19,11),
                                             duration decimal(19,11))
                                             returns decimal(19,11)
                                             stable
                                             as $$
                                             
                                             import decimal
                                             BOOKING_FEE = 2.35
                                             MIN_FAIR = 7.72
                                             PER_MIN_COST = 0.25
                                             PER_MILE_COST = 0.96
                                             
                                             # Duration
                                             time_cost = duration * decimal.Decimal(PER_MIN_COST)
                                             distance_cost = distance * decimal.Decimal(PER_MILE_COST)
                                             
                                             return (time_cost + distance_cost + decimal.Decimal(MIN_FAIR) + decimal.Decimal(BOOKING_FEE))
                                             
                                             $$ language plpythonu;
    """)
    
    