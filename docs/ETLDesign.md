## ETL Design

-----------------------

### Navigation

1. [Project Setup](../README.md)

2. [Project Scope](ProjectScope.md) 

3. [Data Dictionary](DataDictionary.md)

4. [Data Model](DataModel.md)

5. ETL Design

<br>

### 6.0 ETL Design

<p>The legacy ETL codebase is custom written python code using pandas/numpy and SQL to tranform the data and write output to destination tables in Postgres. There are numerious difficulties maintaining the legacy codebase and it does not have any UI to help flag issues quickly. Apache Airflow will be implemented as the main orchestration tool to help improve code maintainability and provide a single consistent programming model in which to define the ETL pipelines. The Airflow cluster will be deployed and hosted in AWS. However, over time the DAGS will be migrated to "Amazon Managed Workflows for Apache Airflow" (MWAA) but this is out of scope for the inital phase of the project.</p>

<br>

### 6.1 Requirements

<p>As shown below, airflow meets all of our requirements for this use case. Airflow is python based which shorterns the learning curve for teams managing the new implementation. Airflow can be deployed as cluster so it can scale as the workload increases or if new feeds are added. </p>

| Requirements for New Orchestration tool                                      |
|:----------------------------------------------------------------------------:|
| Tool must have a user interface from which to monitor and debug DAGs.        |
| Tool must have a consistent programming model in which to define pipelines.  |
| Tool must be able to interface with Redshift and AWS services.               |
| Tool must be python based as team members only have python/SQL skills.       |
| Tool must have backfill capability into order reload historical data.        |
| Tool must be able to handle dependencies between job runs.                   |
| Tool must be able to scale easily to handle additional workload              |

<br>

### 6.2 DAG List

<p>DAGs 1-4 are the primary data pipelines. DAGs 5-6 are to refresh the taxi base and zone lookup data in the staging tables. The design frequency is set to "monthly" as files are created each month and deposited into the source S3 bucket. Each of the primary 4 DAGs can run independantly and load data into the Data warehouse Star schema. </p>


| ID  | File Name               | Description                                      | Dag ID                   | Frequency  |
|:---:|:-----------------------:|:------------------------------------------------:|:------------------------:|:----------:|
| 1   | yellow_dag.py           | Loads yellow taxi data into the warehouse        | tlc_yellow_taxi_data_etl | @Monthly   |
| 2   | green_dag.py            | Loads green taxi data into the warehouse         | tlc_green_taxi_data_etl  | @Monthly   |
| 3   | fhv_dag.py              | Loads FHV vehicle data into the warehouse        | tlc_fhv_taxi_data_etl    | @Monthly   |
| 4   | fhvhv_dag.py            | Loads FHVHV vehicle data into the warehouse      | tlc_fhvhv_taxi_data_etl  | @Monthly   |
| 5   | taxi_base_lookup_dag.py | Loads taxi base lookup data into staging tables  | tlc_taxi_base_lookup_etl | @Monthly   |
| 6   | taxi_zone_lookup_dag.py | Loads taxi zone lookup data into staging tables  | tlc_taxi_zone_lookup_etl | @Monthly   |


1. yellow_dag

![YellowDag](../images/yellow_dag.PNG)

2. green_dag

![GreenDag](../images/green_dag.PNG)

3. fhv_dag

![FHVDag](../images/fhv_dag.PNG)

4. fhvhv_dag

![FHVHVDag](../images/fhvhv_dag.PNG)

5. taxi_base_lookup_dag

![TaxiBase](../images/taxi_base_dag.PNG)

6. taxi_zone_lookup_dag

![TaxiZone](../images/taxi_zone_dag.PNG)