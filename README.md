# SpaxeX ETL and analysis with Airflow and Python
A dataset in a JSON file. It has been downloaded from SpaceX API and contains information about SpaceX rocket launches since 2006.
The dataset is described here: GitHub - SpaceX API.

You can find the JSON dataset here: [GitHub - SpaceX API.](https://github.com/r-spacex/SpaceX-API)
You can find the JSON dataset here: [SpaceX Launch Data](https://api.spacexdata.com/v5/launches/).

## Project Structure
```
/my-spacex-etl-solution
├── README.md                # Main documentation
├── dags/                    # Airflow DAGs
│   ├── spacex_etl_dag.py    # Main ETL DAG
├── scripts/                 # Python scripts for ETL
│   ├── etl_pipeline.py      # Python script for the ETL (extraction, transformation, loading)
├── notebooks/               # Jupyter Notebooks for data analysis and visualization
│   ├── analysis.ipynb       # Basic analysis and visualization
├── data/                    # Placeholder for sample JSON data
│   ├── sample_data.json     # Sample SpaceX API data
├── sql_queries/             # SQL scripts for Redshift
│   ├── data_queries.sql     # SQL queries for analysis
├── requirements.txt         # Python dependencies
```

## Requirements and answers
**Part 1: Data Infrastructure on AWS**

Provide an architectural diagram for a scalable data solution on AWS that includes the following components: data storage and data processing.

**Key Components**

- Airflow DAGs: Orchestrates the ETL process.
- ETL Pipeline: Python script that extracts, transforms, and loads data.
- Pandas Analysis: Analyze the data and generate visualizations
- IAM, VPC, S3 Redhift credentials stored in Airflow Connectors
```
    +------------------------+                  +------------------------+
    |                        |                  |                        |
    |    SpaceX API          |                  |    Amazon S3           |
    |                        |                  |                        |
    +-----------+------------+                  +-----------+------------+
                |                                           |
                v                                           v
    +-----------+------------+                  +-----------+------------+
    |                        |                  |                        |
    |    Airflow DAG         |                  |    Amazon Redshift     |
    | (Extract, Transform,   |                  | (Load and Analytics)   |
    | Load)                  |                  |                        |
    +------------------------+                  +------------------------+
```

## Installation and Setup

```
pip install -r requirements.txt
```

## Running the Pipeline

```
airflow webserver
airflow scheduler
```

**Part 2: ETL Pipeline**
Requirment Provide a tool/script that extracts data from the provided JSON file, transforms the data by applying some cleaning or aggregation, and loads it into the database.

All ETL pipeline has been done using Python and Airflow and can be found in
```
├── dags/                    # Airflow DAGs
│   ├── spacex_etl_dag.py    # Main ETL DAG
├── scripts/                 # Python scripts for ETL
│   ├── etl_pipeline.py      # Python script for the ETL (extraction, transformation, loading)
```
Explain how you would schedule and monitor this pipeline using tools like Apache Airflow.
Airflow allows us to schedule based on schedule_intervals. This being said, we could schedule this job to run @daily. Airflow allows us to monitor success, failure runs using their UI.

Explain how data testing could be implemented
Data testing wasn't implemented, but pytest could be used to check code integrity. Custom unit test functions could be developed to check for missing, duplicate information, data drifts etc.

We could also use Great Expectations for Airflow with the following code:

```
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

ge_task = GreatExpectationsOperator(
task_id='data_validation',
expectation_suite_name='spacex_data_suite',
batch_kwargs={
    'path': '/path/to/data_file.json',
    'datasource': 'your_s3_datasource'
},
dag=dag,
)
```

**Part 3: SQL Queries**

Write an SQL query to find the maximum number of times a core has been reused.
Write an SQL query to find the cores that have been reused in less than 50 days after the previous launch.

Requested queries can be found:
```
├── sql_queries/             # SQL scripts for Redshift
│   ├── data_queries.sql     # SQL queries for analysis
```

**Part 4: Pandas**

Load the dataset into a Pandas DataFrame, handle missing values, and normalize nested JSON structures.
Perform basic statistics, create summaries, and generate visualizations such as bar charts for launches per year and line charts for
Add new columns (e.g., launch success, launch year/month), analyze core reuse, identify quick core reuses, determine busy launch months, calculate average days between launches, assess success rates per site, and create additional visualizations like bar charts and scatter plots.
Include Python libraries that you consider useful and explain it.

Simple data tranformation and analysis can be found in:
```
├── notebooks/               # Jupyter Notebooks for data analysis and visualization
│   ├── analysis.ipynb       # Basic analysis and visualization 
```