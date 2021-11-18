## Udacity Capstone Project - TLC Taxi trips Data Warehouse Project


**Name: Darren Foley**

**Creation Date: 2021-10-21**

-------------------------------------------------------

### Documentation

1. Project Setup

2. [Project Scope](docs/ProjectScope.md) 

3. [Data Dictionary](docs/DataDictionary.md)

4. [Data Model](docs/DataModel.md)

5. [ETL Design](docs/ETLDesign.md) 

6. [Sample Queries](docs/SampleQueries.md)

<br>

### Project Index

```
airflow
├── dags
│   ├── aws.cfg
│   ├── aws-master.cfg
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── extract_and_enrich_from_s3.cpython-36.pyc
│   │   └── extract_and_unzip_from_s3.cpython-36.pyc
│   ├── tlc_dwh
│   │   ├── common
│   │   │   └── __pycache__
│   │   │       └── taxi_zone_lookup_dag.cpython-36.pyc
│   │   ├── etl
│   │   │   ├── fhv_dag.py
│   │   │   ├── fhvhv_dag.py
│   │   │   ├── green_dag.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── fhv_dag.cpython-36.pyc
│   │   │   │   ├── fhvhv_dag.cpython-36.pyc
│   │   │   │   ├── green_dag.cpython-36.pyc
│   │   │   │   ├── hvfhv_dag.cpython-36.pyc
│   │   │   │   ├── taxi_base_lookup_dag.cpython-36.pyc
│   │   │   │   ├── taxi_zone_lookup_dag.cpython-36.pyc
│   │   │   │   └── yellow_dag.cpython-36.pyc
│   │   │   ├── taxi_base_lookup_dag.py
│   │   │   ├── taxi_zone_lookup_dag.py
│   │   │   └── yellow_dag.py
│   │   └── __init__.py
│   └── tmp
│       ├── modified
│       │   ├── taxi_zones_adj.cpg
│       │   ├── taxi_zones_adj.dbf
│       │   ├── taxi_zones_adj.prj
│       │   ├── taxi_zones_adj.shp
│       │   └── taxi_zones_adj.shx
│       ├── taxi_zones.dbf
│       ├── taxi_zones.prj
│       ├── taxi_zones.sbn
│       ├── taxi_zones.sbx
│       ├── taxi_zones.shp
│       ├── taxi_zones.shp.xml
│       └── taxi_zones.shx
├── datasets
│   └── taxi_base_lookup.csv
├── pip_dependencies.sh
├── plugins
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── sql_data_quality.cpython-36.pyc
│   │   │   ├── sql_dimension_tables.cpython-36.pyc
│   │   │   ├── sql_fact_tables.cpython-36.pyc
│   │   │   ├── sql_functions.cpython-36.pyc
│   │   │   ├── sql_insert_queries.cpython-36.pyc
│   │   │   ├── sql_prod_data_quality.cpython-36.pyc
│   │   │   ├── sql_staging_data_quality.cpython-36.pyc
│   │   │   ├── sql_staging_tables.cpython-36.pyc
│   │   │   ├── sql_stored_procedures.cpython-36.pyc
│   │   │   └── sql_truncate_staging.cpython-36.pyc
│   │   ├── sql_data_quality.py
│   │   ├── sql_dimension_tables.py
│   │   ├── sql_fact_tables.py
│   │   ├── sql_functions.py
│   │   ├── sql_insert_queries.py
│   │   ├── sql_prod_data_quality.py
│   │   ├── sql_staging_data_quality.py
│   │   ├── sql_staging_tables.py
│   │   ├── sql_stored_procedures.py
│   │   └── sql_truncate_staging.py
│   ├── __init__.py
│   ├── operators
│   │   ├── clean_staging_data.py
│   │   ├── extract_and_unzip_from_s3.py
│   │   ├── facts_calculator.py
│   │   ├── fhv_enrichment.py
│   │   ├── has_rows.py
│   │   ├── __init__.py
│   │   ├── load_dependencies.py
│   │   ├── load_dimension.py
│   │   ├── load_fact.py
│   │   ├── prod_data_quality_check.py
│   │   ├── __pycache__
│   │   │   ├── clean_staging_data.cpython-36.pyc
│   │   │   ├── extract_and_unzip_from_s3.cpython-36.pyc
│   │   │   ├── facts_calculator.cpython-36.pyc
│   │   │   ├── fhv_enrichment.cpython-36.pyc
│   │   │   ├── has_rows.cpython-36.pyc
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── load_dependencies.cpython-36.pyc
│   │   │   ├── load_dimension.cpython-36.pyc
│   │   │   ├── load_fact.cpython-36.pyc
│   │   │   ├── prod_data_quality_check.cpython-36.pyc
│   │   │   ├── s3_copy_object_operator.cpython-36.pyc
│   │   │   ├── s3_extract_zip_files.cpython-36.pyc
│   │   │   ├── s3_to_local.cpython-36.pyc
│   │   │   ├── s3_to_redshift.cpython-36.pyc
│   │   │   ├── s3_to_staging.cpython-36.pyc
│   │   │   ├── s3_to_staging_with_enrichment.cpython-36.pyc
│   │   │   └── staging_data_quality_check.cpython-36.pyc
│   │   ├── s3_copy_object_operator.py
│   │   ├── s3_extract_zip_files.py
│   │   ├── s3_to_local.py
│   │   ├── s3_to_redshift.py
│   │   ├── s3_to_staging.py
│   │   ├── s3_to_staging_with_enrichment.py
│   │   └── staging_data_quality_check.py
│   ├── __pycache__
│   │   └── __init__.cpython-36.pyc
│   └── scripts
│       ├── extract_and_unzip_from_s3.py
│       └── __pycache__
│           └── extract_and_unzip_from_s3.cpython-36.pyc
├── requirements.txt
└── setup.py
```

```
docs/
├── DataDictionary.md
├── DataModel.md
├── ETLDesign.md
├── ProjectScope.md
└── SampleQueries.md
```

```
images/
├── airflow_ui.PNG
├── aws_access.PNG
├── conceptual_model.png
├── fhv_dag.PNG
├── fhvhv_dag.PNG
├── green_dag.PNG
├── logical_model.png
├── NYC_Zones.jpg
├── NYC_Zones.png
├── project_index.png
├── taxi_base_dag.PNG
├── taxi_zone_dag.PNG
└── yellow_dag.PNG
```

```
misc
├── conceptual_model.drawio
└── logical_diagram.drawio
```

<br>

### Project Setup

**Versioning & Compatiblity**

<p>Airflow DAG's were written and tested in ubuntu 16.04 VM running Airflow version 1.10.2 installed in python 3.6</p>

```
# uname -a 
Linux 0ed8a3d2ab28 4.15.0-1098-gcp #111~16.04.1-Ubuntu SMP Tue Apr 13 19:05:08 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```


```
# airflow version
  ____________       _____________
 ____    |__( )_________  __/__  /________      __
____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /
___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /
 _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/
   v1.10.2
```

```
# python --version
Python 3.6.3
```

<br>

**Prerequisites**

<p>There are a number of prerequisites required before the Airflow pipelines can be run.</p>

1. Create an AWS User

<p>Create an AWS user that has permission to copy data from S3 into redshift. The user should also have permissions to connect and query redshift. For testing purposes or for simplicity you can add the below policies. </p>

![AWS Access](images/aws_access.PNG)


2. Update the aws-master.cfg file located at /airflow/dags/aws-master.cfg with your AWS user key & secret key.

<p>The setup.py script depends upon the config being set before running.</p>

<br>

**Run setup.py (Optional)**

<p>Within the Airflow folder there is a setup file (/airflow/setup.py) which should handle all of the airflow DAG dependencies. Just run from your command line environment as shown:</p>

```
# python ./setup.py "your-local-bucket-name"
```

This script does two things:

1. Installs Python Packages

<p>The ETL pipelines process and load geometric shape data which relies on the geopandas (geopandas==0.9.0) package in python 3.6. This must be installed before the DAG's can run correctly. The newest version of pip must also be upgraded before installation. </p>

```
pip install --upgrade pip

pip install geopandas

```

2. Creates an S3 Staging Bucket

<p>The next dependency is to create a local S3 bucket to hold lookup data before being loaded into Redshift. This will act as a staging area for shape files. Remember that the bucket name must be set in airflow UI before DAGS can be run. </p>

<p>Either perform the above steps manually or just run the setup script.</p>

<br>

**Create the Redshift Cluster**

<p>As described within the project scope, the design requires a ra3.xlplus RA3 node cluster. Use the "create_cluster.sh" script in project root to spin up the cluster before running the DAGs. Either setup a cluster manually through the AWS console or run the create_cluster script.</p>

```
# ./create_cluster.sh -h
./create_cluster.sh [-h|help] [-T|testing] [-P|production] [-d|delete] <cluster-identifier>

# ./create_cluster.sh -P
creating cluster......
```

<br>

**Set Airflow Connections**

1. AWS User

<p>You'll need to add your AWS user which has access to load data into Redshift from S3. These credentials must be be set in the airflow UI as "aws", which will be picked up by the dags during execution.</p>


2. Redshift Hostname

<p>The redshift Hostname will need to be added into the Airflow UI as "redshift", which will be picked up by the dags during execution. </p>


**Set Airflow Variables**

1. S3 Local Bucket Name

<p>As mentioned above, set the bucket name variable as "local_bucket"="your-bucket-name", which will be picked up by the dags during execution. </p>


2. Add HOME_ variable to indicate DAG home directory

<p>Location of the Home directory where dags are located. (Default: /home/workspace/airflow/dags)</p>

<br>

### Running Airflow Pipelines

<p>Once all of the above has been created, you can run the dags from the airflow UI. In production, the dags will run on a monthly schedule, however by default they are set to run for March 2020 only. You can run each dag manually from the UI or you can run the dags between an interval date range to test the ability to load files historically. </p>

<p>Switch on all DAGs as shown below and run either yellow, green, fhv or fhv_hv pipelines which are the primary dags. Taxi zone and base are triggered by the other DAG's. Note that due to the size of the fhv_hv source file (tens of millions of rows) it can take up to +3 hours to load the data for this one. Yellow, green or fhv all should process much faster. </p>

![Airflow UI](images/airflow_ui.PNG)
