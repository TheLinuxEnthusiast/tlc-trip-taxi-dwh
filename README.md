## Udacity Project - TLC Taxi trips Data Warehouse Project
---------------------------------------------------------

**Name: Darren Foley**

**Creation Date: 2021-10-21**

-------------------------------------------------------

<br>

### Project Overview

<p>The NYC Taxi and Limousine Commission (TLC) are migrating their on-premise data warehouse to Amazon web services (AWS) in order to improve their analytical reporting capability. Records include fields capturing pick-up and drop-off dates/times for Yellow Taxi cabs, Green taxi cabs & for-hire vehicles (FHV) which arrive as a monthly files in CSV format. Data is collected from third party technology providers who meter each vehicle and store information relating to each indiviual trip. One row represents a single trip made by a TLC-licensed vehicle.</p>

<br>

<p>The on premise datawarehouse is stored in Postgres v9 which is currently under high load and is stuggling to meet daily reporting requirements. A lift and shift to Redshift in AWS should provide improved reporting capacity and flexibility. Redshift's massively parallel processing (MPP) architecture allows for more nodes to be added as load increases. Redshift is also backward compatable with redshift, which should make migration easier than moving to another vendor. </p>

<br>

<p>The ETL process is written in python and SQL using custom data transformations, jobs are sceduled using cron. TLC would like to migrate their legacy data feeds to Apache Airflow which will give better visiblity over their existing etl pipeline through the airflow UI, in addition to airflows modular architecture and extensible operators.</p>

<br>

### Documentation

<br>

1. ![Project Scope](docs/ProjectScope.md) 

2. ![Data Dictionary](docs/DataDictionary.md)

3. ![Data Model](docs/DataModel.md)

4. ![ETL Design](docs/ETLDesign.md) 
