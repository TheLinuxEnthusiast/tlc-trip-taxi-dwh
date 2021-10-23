## Project Scope

--------------------------------------------

<br>

### Navigation

1. [Home](../README.md)

2. Project Scope

3. [Data Dictionary](DataDictionary.md)

4. [Data Model](DataModel.md)

5. [ETL Design](ETLDesign.md) 

<br>

### 1.0 Introduction

<p>The NYC Taxi and Limousine Commission (TLC) are migrating their on-premise data warehouse to Amazon web services (AWS) in order to improve their analytical reporting capability. Records include fields capturing pick-up and drop-off dates/times for Yellow Taxi cabs, Green taxi cabs & for-hire vehicles (FHV) which arrive as monthly files in CSV format. Data is collected from third party technology providers who meter each vehicle and store information relating to each indiviual trip. One row represents a single trip made by a TLC-licensed vehicle.</p>

<p>The on premise datawarehouse is stored in Postgres v9 which is currently under high load and is stuggling to meet daily reporting requirements. A "lift and shift" to Redshift in AWS should provide improved reporting capacity and flexibility. Redshift's massively parallel processing (MPP) architecture allows for more nodes to be added as load increases. Since Redshift is derived from postgres, it should make migration easier in comparison with other vendors.</p>

<p>The existing ETL process is written in python and SQL using custom data transformations, with jobs scheduled using cron. TLC would like to migrate their legacy data feeds to Apache Airflow which will give better visiblity over their existing etl pipeline through the airflow UI, in addition to airflows modular architecture and extensible operators.</p>

<br>

### 2.0 Acronyms and Terminology

| Term            | Description                                                                          |
|----------------:|:------------------------------------------------------------------------------------:|
| NYC             | New York City                                                                        |
| TLC             | Taxi and Limousine Commission                                                        |
| Yellow Taxi     | New York city's medallion yellow taxis                                               |
| Green Taxi      | Street Hail Livery Taxis                                                             |
| FHV             | For hire Vehicles (Uber, lyft etc.)                                                  |
| hvFHV           | Any FHV company that does +10,000 trips a day is High volume (hvFHV)                 |
| Borough         | Subset of NYC region were a taxi can pick up fairs (Queens, Brooklyn, Bronx etc)     |
| Zone            | A borough contains smaller subsets called zones (There are 265 zones in NYC)         |


![Diagram of Zones in NYC](../images/NYC_Zones.jpg)

*Diagram shows all taxi zones in NYC*

<br>

### 3.0 Requirements

#### 3.1 Expected Load and data Volume

<p>The new system must be able to handle the existing data volume and reporting load. Data volume and analytical workload is expected to increase over time. The system should have the flexiblity to scale with little to no downtime or administrative overhead. </p>

<u>Existing Data Volume:</u> 

<p>Files can vary in size between 100MB to +1GB or more. Due to COVID-19 passenger numbers have been much lower than usual for 2020. File size is expected to grow much larger post covid due to the return in demand.</p>

4 Monthly files (Yellow, Green, FHV, hvFHV)

| FileType  | FileType | NumberOfRows   | NumberOfFields | Size       |
|----------:|:--------:|:--------------:|:--------------:|:----------:|
| Yellow    | CSV      | 6-20 million   | 18             | 100-600MB  |
| Green     | CSV      | 6-20 million   | 20             | 100-600MB  |
| FHV       | CSV      | 1-5 million    | 7              | 100-300MB  |
| hvFHV     | CSV      | +10 million    | 7              | +1GB       |



