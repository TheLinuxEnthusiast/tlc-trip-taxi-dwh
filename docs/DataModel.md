## Data Model

-----------------------

### Navigation

1. [Home](../README.md)

2. [Project Scope](ProjectScope.md) 

3. [Data Dictionary](DataDictionary.md)

4. Data Model

5. [ETL Design](ETLDesign.md) 

<br>

### 5.0 Data Model

<p>The data model will have a traditional kimball star schema design with a single fact table recording trip events, a single event corresponding to each row of data. There will be seven dimensions in total -> time, location/zone, vendor, rate, payment type, taxi base, trip type. The data does not have a unique identifier for each trip across all taxi base types so a surrogate key will be generated. In order for the FHV datasets to fit with the yellow and green taxi datasets, fields will need to be merged and extra data will need to be added from the Uber API. These datasets did not contain any information relating to fairs or charges. This will need to be estimated using the Uber api and added to the datasets during the ETL process.</p>

<br>

#### 5.1 Conceptual model

![Conceptual Model](../images/conceptual_model.png)

*Diagram shows a roguh conceptual model of proposed facts and dimensions*

<br>

#### 5.2 Logical Model

<br>

#### 5.3 Physical Model

