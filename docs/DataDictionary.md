## Data Dictionary

-----------------------

### Navigation

1. [Project Setup](../README.md)

2. [Project Scope](ProjectScope.md) 

3. Data Dictionary

4. [Data Model](DataModel.md)

5. [ETL Design](ETLDesign.md) 

<br>

### 4.0 Data Dictionary

#### yellow_tripdata_YYYY-MM.csv


| Field Name              | Field Description                                    | Data Type  |
|:-----------------------:|:----------------------------------------------------:|:----------:|
| VendorID*               | A code indicating the TPEP provider (1,2)            | string     |
| tpep_pickup_datetime    | Date when meter was engaged                          | datetime   |
| tpep_dropoff_datetime   | Date when meter was disengaged                       | datetime   |
| passenger_count         | Number of passengers in the vehicle (Driver entered) | int        |
| trip_distance           | Elasped Trip in miles                                | float      |
| RatecodeID*             | Rate code applied to trip (1,2,3,4,5,6)              | string     |
| store_and_fwd_flag      | Data held in memory before being sent to vendor(Y,N) | string     |
| PULocationID            | Pick up location Zone code                           | string     |
| DOLocationID            | Drop off location Zone code                          | string     |
| payment_type*           | How the trip was paid for (1,2,3,4,5,6)              | string     |
| fare_amount             | Time and distance fare calculated                    | float      |
| extra                   | Misc Surcharges; e.g. 0.50 for rush hour             | float      |
| mta_tax                 | Tax automatically triggered based on meter usage     | float      |
| tip_amount              | Credit card tips only, cash not included             | float      |
| tolls_amount            | Tolls paid during the trip                           | float      |
| improvement_surcharge   | Surcharge assessed trips at the flag drop            | float      |
| total_amount            | Total amount, does not include cash tips             | float      |
| congestion_surcharge    | Surcharge for traffic/congestion                     | float      |

VendorID:

1. Creative Mobile Technologies LLC

2. VeriFone Inc


Ratecodes:

1. Standard rate

2. JFK

3. Newark

4. Nassau or Westchester

5. Negotiated fare

6. Group ride


Payment Type:

1. Credit Card

2. Cash

3. No charge

4. Dispute

5. Unknown

6. Voided trip


<br>

#### green_tripdata_YYYY-MM.csv


| Field Name              | Field Description                                    | Data Type  |
|:-----------------------:|:----------------------------------------------------:|:----------:|
| VendorID                | A code indicating the LPEP provider (1,2)            | string     |
| lpep_pickup_datetime    | Date when meter was engaged                          | datetime   |
| lpep_dropoff_datetime   | Date when meter was disengaged                       | datetime   |
| store_and_fwd_flag      | Data held in memory before being sent to vendor(Y,N) | string     |
| RatecodeID              | Rate code applied to trip (1,2,3,4,5,6)              | string     |
| PULocationID            | Pick up location Zone code                           | string     |
| DOLocationID            | Drop off location Zone code                          | string     |
| passenger_count         | Number of passengers in the vehicle (Driver entered) | int        |
| trip_distance           | Elasped Trip in miles                                | float      |
| fare_amount             | Time and distance fare calculated                    | float      |
| extra                   | Misc Surcharges; e.g. 0.50 for rush hour             | float      |
| mta_tax                 | Tax automatically triggered based on meter usage     | float      |
| tip_amount              | Credit card tips only, cash not included             | float      |
| tolls_amount            | Tolls paid during the trip                           | float      |
| ehail_fee               | Fee for hail using app                               | float      |
| improvement_surcharge   | Surcharge assessed trips at the flag drop            | float      |
| total_amount            | Total amount, does not include cash tips             | float      |
| payment_type            | How the trip was paid for (1,2,3,4,5,6)              | string     |
| trip_type               | Street-hail (1) or dispatch (2)                      | string     |
| congestion_surcharge    | Surcharge for traffic/congestion                     | float      |

VendorID (Same as above)

RatecodeID (Same as above)

Payment Type:(Same as above)

<br>

#### fhvhv_tripdata_YYYY-MM.csv


| Field Name              | Field Description                                                   | Data Type  |
|:-----------------------:|:-------------------------------------------------------------------:|:----------:|
| hvfhs_license_num       | TLC licence number for High volume vendor (Uber, Lyft etc)          | string     |
| dispatching_base_num    | The TLC Base License Number of the base that dispatched the trip    | string     |
| pickup_datetime         | The date and time of the trip pick-up                               | datetime   |
| dropoff_datetime        | The date and time of the trip drop-off                              | datetime   |
| PULocationID            | TLC Taxi Zone in which the trip began                               | string     |
| DOLocationID            | TLC Taxi Zone in which the trip ended                               | string     |
| SR_Flag                 | Indicates if the trip was a part of a shared ride chain (1 or NULL) | string     |

<br>

#### fhv_tripdata_YYYY-MM.csv


| Field Name              | Field Description                                                   | Data Type  |
|:-----------------------:|:-------------------------------------------------------------------:|:----------:|
| dispatching_base_num    | The TLC Base License Number of the base that dispatched the trip    | string     |
| pickup_datetime         | The date and time of the trip pick-up                               | datetime   |
| dropoff_datetime        | The date and time of the trip dropoff                               | datetime   |
| PULocationID            | TLC Taxi Zone in which the trip began                               | string     |
| DOLocationID            | TLC Taxi Zone in which the trip ended                               | string     |
| SR_Flag                 | Indicates if the trip was a part of a shared ride chain (1 or NULL) | string     |
| Affiliated_base_number  | TLC Licence number for FHV vendor                                   | string     |

<br>

#### Lookup file 1 - taxi_zone_lookup.csv & taxi_zone.shp

| Field Name              | Field Description                                          | Data Type  |
|:-----------------------:|:----------------------------------------------------------:|:----------:|
| LocationID              | Location ID for taxi zone                                  | string     |     
| Borough                 | Name of borough distincts in NYC                           | string     |
| Zone                    | Name of taxi zone                                          | string     |
| service_zone            | Name of Service Zone                                       | string     |
| Shape Length            | Length of shape polgon object                              | float      |
| Shape Area              | Area of shape polygon object                               | float      |
| Geometry                | polygon data type, represents the taxi zone as a polygon   | polygon    |

<br>

#### Lookup File 2 - taxi_base_lookup.csv

| Field Name                  | Field Description                                               | Data Type  |
|:---------------------------:|:---------------------------------------------------------------:|:----------:|
| High Volume License Number  | Licence number for transport provider that are high frequency   | string     |
| License Number              | Alternative Licence number                                      | string     |
| Base Name                   | Base of operations where the transport provider deploys from    | string     |
| App Company Affiliation     | App name associated with tranport provider                      | string     |

<br>

#### Derived data - calculated fields

Derive the lat/long centroid from start Zone and end Zone. Pass these values to the estimate_cost function.


| Name              | Description                                        | Data Type     |
|:-----------------:|:--------------------------------------------------:|:-------------:|
| Start Latitude    | Estimated Latitude base on centroid of taxi zone   | decimal(11,8) |
| Start Longitude   | Estimated Longitude base on centroid of taxi zone  | decimal(10,8) | 
| End Latitude      | Estimated Latitude base on centroid of taxi zone   | decimal(11,8) |
| End Longitude     | Estimated Longitude base on centroid of taxi zone  | decimal(10,8) |
| Distance          | Geometric distance between start and end lat/long  | float         |
| Duration          | Estimated duration                                 | float         |
| Estimated of cost | Estimated cost of journey                          | float         |