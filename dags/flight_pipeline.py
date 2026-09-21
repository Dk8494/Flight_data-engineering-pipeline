from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import sys

# Add src to Python path for Airflow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.extract import extract_data
from src.validation.quality_checks import run_quality_checks
from src.transformation.transform import transform_data
from src.warehouse.loader import execute_ddl, load_dimensions, load_facts
from src.utils.config import DATA_SOURCE_PATH, PROJECT_ROOT

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'flight_data_pipeline',
    default_args=default_args,
    description='End-to-End Flight Data Engineering Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def _extract(**context):
    df = extract_data(DATA_SOURCE_PATH)
    # Pushing raw data shape to XCom for observability
    context['ti'].xcom_push(key='raw_count', value=len(df))
    # We can serialize small df or write to staging area; here we return for simplicity if data is small,
    # but for 300k rows, it's better to save to staging file.
    staging_path = os.path.join(PROJECT_ROOT, 'data', 'sample', 'staging_raw.csv')
    df.to_csv(staging_path, index=False)
    return staging_path

def _validate(**context):
    staging_path = context['ti'].xcom_pull(task_ids='extract')
    import pandas as pd
    df = pd.read_csv(staging_path)
    df_clean = run_quality_checks(df)
    valid_path = os.path.join(PROJECT_ROOT, 'data', 'sample', 'staging_valid.csv')
    df_clean.to_csv(valid_path, index=False)
    return valid_path

def _transform(**context):
    valid_path = context['ti'].xcom_pull(task_ids='validate')
    import pandas as pd
    df_clean = pd.read_csv(valid_path)
    df_transformed = transform_data(df_clean)
    transform_path = os.path.join(PROJECT_ROOT, 'data', 'sample', 'staging_transformed.csv')
    df_transformed.to_csv(transform_path, index=False)
    return transform_path

def _load_schema(**context):
    ddl_dims = os.path.join(PROJECT_ROOT, 'sql', 'ddl', 'create_dimensions.sql')
    ddl_facts = os.path.join(PROJECT_ROOT, 'sql', 'ddl', 'create_fact_tables.sql')
    execute_ddl(ddl_dims)
    execute_ddl(ddl_facts)

def _load_data(**context):
    transform_path = context['ti'].xcom_pull(task_ids='transform')
    import pandas as pd
    df = pd.read_csv(transform_path)
    load_dimensions(df)
    load_facts(df)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=_extract,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate',
    python_callable=_validate,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=_transform,
    dag=dag,
)

load_schema_task = PythonOperator(
    task_id='load_schema',
    python_callable=_load_schema,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=_load_data,
    dag=dag,
)

extract_task >> validate_task >> transform_task >> load_schema_task >> load_data_task
