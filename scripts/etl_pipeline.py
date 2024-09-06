import requests
import json
import boto3
import pandas as pd
from psycopg2 import connect
from datetime import datetime

# AWS S3 configuration
s3 = boto3.client('s3')
bucket_name = 'test-bucket-name'

# Redshift connection details
redshift_conn_params = {
    'dbname': 'refshift_db',
    'host': 'redshift_host',
    'port': '5439',
    'user': 'user',
    'password': 'password'
}

def extract_data():
    """Extract data from the SpaceX API."""
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    data = response.json()
    
    # Save data locally as JSON
    with open('/tmp/spacex_launch_data.json', 'w') as f:
        json.dump(data, f)
    
    # Upload data to S3
    s3.upload_file('/tmp/spacex_launch_data.json', bucket_name, 'spacex_launch_data.json')

def transform_data():
    """Transform and clean the data."""
    with open('/tmp/spacex_launch_data.json', 'r') as f:
        data = json.load(f)
    
    # Convert to pandas DataFrame for transformation
    df = pd.json_normalize(data)

    # Normalize failures and cores nasted dictionary
    df['failures_normalized'] = df['failures'].apply(lambda x: x[0] if len(x) > 0 else {})
    failures_df = pd.json_normalize(df['failures_normalized']).add_prefix('f_')
    df = pd.concat([df.drop(columns=['failures_normalized','failures']), failures_df], axis=1)

    df['cores_normalized'] = df['cores'].apply(lambda x: x[0] if len(x) > 0 else {})
    cores_df = pd.json_normalize(df['cores_normalized']).add_prefix('c_')
    df = pd.concat([df.drop(columns=['cores_normalized','cores']), cores_df], axis=1)
    
    # Clean and process data (handle missing values, add new columns)
    df = df.applymap(lambda x: np.nan if (x is None or (isinstance(x, list) and len(x) == 0)) else x)
    df['date_utc'] = pd.to_datetime(df['date_utc'])
    df['launch_year'] = df['date_utc'].dt.year
    df['launch_month'] = df['date_utc'].dt.year
    
    # Save the cleaned data
    df.to_csv('/tmp/spacex_cleaned_data.csv', index=False)
    
    # Upload cleaned data to S3
    s3.upload_file('/tmp/spacex_cleaned_data.csv', bucket_name, 'spacex_cleaned_data.csv')

def load_to_redshift():
    """Load the cleaned data into Redshift."""
    conn = connect(**redshift_conn_params)
    cur = conn.cursor()
    
    # Load the cleaned data from S3 to Redshift
    copy_query = """
    COPY your_table_name
    FROM 's3://test-s3-bucket/spacex_cleaned_data.csv'
    IAM_ROLE 'iam-role-arn'
    CSV IGNOREHEADER 1;
    """
    
    cur.execute(copy_query)
    conn.commit()
    cur.close()
    conn.close()
