# Project 1 - Data Warehouse Analytics 
This is the first project for course **Data Warehouse and Analysis**.
<br>
<br>

### Tech stack
It uses **Oracle database**, and **Apache NiFi** for data ingestion and populating the dimension and facts tables. **Power BI** is used for data visualization.
<br>
<br>

### How to do it by yourself
1. Clone the repository
2. Install Oracle database
3. With provided SQL statements, create the Business Database tables and populate them with provided (randomly generated) data
4. With provided SQL statements, create the Datamart Database tables
5. Use Apache NiFi to ingest data from Business Database to Datamart Database
6. Use Power BI to visualize the data (provided Report.pbix file)

# Project 2 - Apache Spark and Google Big Query
This is the second project for course **Data Warehouse and Analysis**. There are two parts to this project:
1. **Part 1** - Works with a real time stream (https://stream.wikimedia.org/v2/stream/)
2. **Part 2** - Works with a dataset of data (https://www.kaggle.com/datasets/ogbuokiriblessing/sensor-based-aquaponics-fish-pond-datasets?select=IoTPond10.csv)
<br>
<br>

### Tech stack
It uses **Apache Spark** for data processing and **Google Big Query** for data storage and querying. **Power BI** is used for data visualization. Additionally, **File System Watcher** is used to monitor output directory of Spark and add new csv files to Big Query.

### How to do it by yourself
1. Clone the repository
2. Install Apache Spark
3. Create a Google Cloud Project and enable Big Query API
4. Create a Big Query dataset and table
5. Create account and key for Big Query and download the JSON file (modify the provided Python script with the path to the JSON file and your credentials)
6. Use provided Python script to process data with Spark and upload it to Big Query
7. Use Power BI to visualize the data (provided Report.pbix file)


# Project 3 - Clustering and Classification
This is the third project for course **Data Warehouse and Analysis**.
<br>
<br>

### Tech stack
It uses **Weka** for clustering and classification.

### How to do it by yourself
1. Clone the repository
2. Install Weka
3. Use provided Python script to see data stats
4. Use provided dataset and Weka to perform clustering and classification
5. View different results in the provided Presentation.pptx file
