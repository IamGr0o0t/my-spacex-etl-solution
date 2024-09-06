from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from scripts.etl_pipeline import extract_data, transform_data, load_to_redshift

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'spacex_etl_pipeline',
    default_args=default_args,
    description='SpaceX ETL pipeline',
    schedule='@daily',
)

# Define the tasks in the DAG

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_redshift',
    python_callable=load_to_redshift,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> load_task
