from airflow import DAG
from airflow.utils.dates import days_ago
from custom_airflow.operators import CustomBigQueryOperator
from custom_airflow.operators import CustomBigQueryToCloudStorageOperator
from custom_airflow.operators import CustomGoogleCloudStorageDownloadDirectoryOperator
from custom_airflow.sensors import (BigQueryWildcardTableSuffixSensor,
                                    CustomBigQueryTableSensor)
from airflow.models import Variable


default_args = {
    'start_date': days_ago(0),
    'project_id': Variable.get('gcp_project_id'),
    'bigquery_conn_id': Variable.get('bigquery_conn_id'),
    'dataset_id': Variable.get('bigquery_dataset_id'),
    'write_disposition': 'WRITE_TRUNCATE',
    'allow_large_results': True,
    'use_legacy_sql': False
}


# *****************************************************************************
# DAG DEFINITION
# *****************************************************************************
dag = DAG(
    'train_model',
    default_args=default_args,
    description='Train model pipeline',
    schedule_interval=None)


# *****************************************************************************
# TRAIN TITLES SENSOR
# *****************************************************************************
train_titles_sensor = BigQueryWildcardTableSuffixSensor(
    task_id='train_titles_sensor',
    dag=dag,
    table_id='stackoverflow_posts_title_*',
    initial_suffix='{{ dag_run.conf["initial_train_pdate"] }}',
    final_suffix='{{ dag_run.conf["final_train_pdate"] }}',
    timeout=60)


# *****************************************************************************
# TRAIN TAGS SENSOR
# *****************************************************************************
train_tags_sensor = BigQueryWildcardTableSuffixSensor(
    task_id='train_tags_sensor',
    dag=dag,
    table_id='stackoverflow_posts_tags_*',
    initial_suffix='{{ dag_run.conf["initial_train_pdate"] }}',
    final_suffix='{{ dag_run.conf["final_train_pdate"] }}',
    timeout=60)


# *****************************************************************************
# TEST TITLES SENSOR
# *****************************************************************************
test_titles_sensor = BigQueryWildcardTableSuffixSensor(
    task_id='test_titles_sensor',
    dag=dag,
    table_id='stackoverflow_posts_title_*',
    initial_suffix='{{ dag_run.conf["initial_test_pdate"] }}',
    final_suffix='{{ dag_run.conf["final_test_pdate"] }}',
    timeout=60)


# *****************************************************************************
# TEST TAGS SENSOR
# *****************************************************************************
test_tags_sensor = BigQueryWildcardTableSuffixSensor(
    task_id='test_tags_sensor',
    dag=dag,
    table_id='stackoverflow_posts_tags_*',
    initial_suffix='{{ dag_run.conf["initial_test_pdate" ]}}',
    final_suffix='{{ dag_run.conf["final_test_pdate"] }}',
    timeout=60)


# *****************************************************************************
# TAGS TABLE SENSOR
# *****************************************************************************
tags_table_sensor = CustomBigQueryTableSensor(
    task_id='tags_table_sensor',
    dag=dag,
    table_id='tags',
    timeout=60)


# *****************************************************************************
# SELECT TAGS
# *****************************************************************************
select_tags = CustomBigQueryOperator(
    task_id='select_tags',
    dag=dag,
    sql='sql/select_tags.sql',
    destination_dataset_table='{0}.{1}.selected_tags'
        .format(Variable.get('gcp_project_id'), Variable.get('bigquery_dataset_id')))
