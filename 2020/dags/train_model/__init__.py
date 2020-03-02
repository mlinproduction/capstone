from airflow import DAG
from airflow.models import Variable
import datetime


from .titles_sensor import TitlesSensor
from .tagged_posts_sensor import TaggedPostsSensor
from .tags_table_sensor import TagsTableSensor


default_args = {
    'start_date': datetime.datetime.strptime('2020-02-01', '%Y-%m-%d'),
    'project_id': Variable.get('gcp_project_id'),
    'bigquery_conn_id': Variable.get('bigquery_conn_id'),
    'write_disposition': 'WRITE_TRUNCATE',
    'allow_large_results': True,
    'use_legacy_sql': False,
    'google_cloud_storage_conn_id': Variable.get('google_cloud_storage_conn_id')
}


dag = DAG(
    'train_model',
    default_args=default_args,
    description='Train model pipeline',
    schedule_interval=None)


train_titles_sensor = TitlesSensor(dag, train=True)
test_titles_sensor = TitlesSensor(dag, train=False)

train_tagged_posts_sensor = TaggedPostsSensor(dag, train=True)
test_tagged_posts_sensor = TaggedPostsSensor(dag, train=False)

tags_table_sensor = TagsTableSensor(dag)


# *****************************************************************************
# SELECT TAGS
# *****************************************************************************
# select_tags = CustomBigQueryOperator(
#     task_id='select_tags',
#     dag=dag,
#     sql='sql/select_tags.sql',
#     destination_dataset_table='{0}.{1}.selected_tags'
#         .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id')))


# *****************************************************************************
# FLATTEN TAGS
# *****************************************************************************
# train_flatten_tags = CustomBigQueryOperator(
#     task_id='train_flatten_tags',
#     dag=dag,
#     sql='sql/flatten_tags.sql',
#     destination_dataset_table='{0}.{1}.train_flattened_tags'
#         .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id')),
#     params={'train_test': 'train'})


# test_flatten_tags = CustomBigQueryOperator(
#     task_id='test_flatten_tags',
#     dag=dag,
#     sql='sql/flatten_tags.sql',
#     destination_dataset_table='{0}.{1}.test_flattened_tags'
#         .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id')),
#     params={'train_test': 'test'})


# *****************************************************************************
# CONSTRUCT TRAIN AND TEST TABLES
# *****************************************************************************
# train_construct_table = CustomBigQueryOperator(
#     task_id='train_construct_table',
#     dag=dag,
#     sql='sql/construct_table.sql',
#     destination_dataset_table='{0}.{1}.train_table'
#         .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id')),
#     params={'train_test': 'train'})
# 
# 
# test_construct_table = CustomBigQueryOperator(
#     task_id='test_construct_table',
#     dag=dag,
#     sql='sql/construct_table.sql',
#     destination_dataset_table='{0}.{1}.test_table'
#         .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id')),
#     params={'train_test': 'test'})


# *****************************************************************************
# EXPORT TO GOOGLE CLOUD STORAGE
# *****************************************************************************
# train_export_to_cloud_storage = CustomBigQueryToCloudStorageOperator(
#     task_id='train_export_to_cloud_storage',
#     dag=dag,
#     source_project_dataset_table="{{ task_instance.xcom_pull(task_ids='train_construct_table', key='table_uri') | replace('`', '') }}",
#     destination_cloud_storage_uris=['gs://' + os.path.join(Variable.get('gcs_bucket'), Variable.get('gcs_prefix'), 'train-table', '*')],
#     compression='NONE',
#     export_format='CSV')
# 
# 
# test_export_to_cloud_storage = CustomBigQueryToCloudStorageOperator(
#     task_id='test_export_to_cloud_storage',
#     dag=dag,
#     source_project_dataset_table="{{ task_instance.xcom_pull(task_ids='test_construct_table', key='table_uri') | replace('`', '') }}",
#     destination_cloud_storage_uris=['gs://' + os.path.join(Variable.get('gcs_bucket'), Variable.get('gcs_prefix'), 'test-table', '*')],
#     compression='NONE',
#     export_format='CSV')
# 
# 
# tags_export_to_cloud_storage = CustomBigQueryToCloudStorageOperator(
#     task_id='tags_export_to_cloud_storage',
#     dag=dag,
#     source_project_dataset_table="{{ task_instance.xcom_pull(task_ids='select_tags', key='table_uri') | replace('`', '') }}",
#     destination_cloud_storage_uris=['gs://' + os.path.join(Variable.get('gcs_bucket'), Variable.get('gcs_prefix'), 'tags', '*')],
#     compression='NONE',
#     export_format='CSV')


# *****************************************************************************
# DOWNLOAD TO LOCAL
# *****************************************************************************
# train_download_to_local = CustomGoogleCloudStorageDownloadDirectoryOperator(
#     task_id='train_download_to_local',
#     dag=dag,
#     bucket=Variable.get('gcs_bucket'),
#     prefix=os.path.join(Variable.get('gcs_prefix'), 'train-table/'),
#     directory=Variable.get('local_working_dir'))
# 
# 
# test_download_to_local = CustomGoogleCloudStorageDownloadDirectoryOperator(
#     task_id='test_download_to_local',
#     dag=dag,
#     bucket=Variable.get('gcs_bucket'),
#     prefix=os.path.join(Variable.get('gcs_prefix'), 'test-table/'),
#     directory=Variable.get('local_working_dir'))
# 
# 
# tags_download_to_local = CustomGoogleCloudStorageDownloadDirectoryOperator(
#     task_id='tags_download_to_local',
#     dag=dag,
#     bucket=Variable.get('gcs_bucket'),
#     prefix=os.path.join(Variable.get('gcs_prefix'), 'tags/'),
#     directory=Variable.get('local_working_dir'))


# *****************************************************************************
# TRAIN MODEL
# *****************************************************************************
# def train_production_wrapper(model_path, train_dataset_paths,
#                              test_dataset_paths, labels_paths, train_params):
#     print(train_params)
#     return train_production(model_path,
#                             eval(train_dataset_paths),
#                             test_dataset_paths,
#                             labels_paths[0],
#                             eval(train_params))
# 
# 
# train_model = PythonOperator(
#     task_id='train_model',
#     dag=dag,
#     python_callable=train_production_wrapper,
#     op_kwargs={
#         'model_path': '',
#         'train_dataset_paths': "{{ task_instance.xcom_pull(task_ids='train_download_to_local', key='downloaded_files') }}",
#         'test_dataset_paths': "{{ task_instance.xcom_pull(task_ids='test_download_to_local', key='downloaded_files') }}",
#         'labels_paths': "{{ task_instance.xcom_pull(task_ids='tags_download_to_local', key='downloaded_files') }}",
#         'train_params': "{{ dag_run.conf['train_params'] }}"})


# *****************************************************************************
# RELATIONS BETWEEN TASKS
# *****************************************************************************
# [train_tagged_posts_sensor, tags_table_sensor] >> select_tags
# [select_tags, train_tagged_posts_sensor] >> train_flatten_tags
# [select_tags, test_tagged_posts_sensor] >> test_flatten_tags
# [train_flatten_tags, train_titles_sensor] >> train_construct_table
# [test_flatten_tags, test_titles_sensor] >> test_construct_table
# train_construct_table >> train_export_to_cloud_storage
# test_construct_table >> test_export_to_cloud_storage
# train_export_to_cloud_storage >> train_download_to_local
# test_export_to_cloud_storage >> test_download_to_local
# select_tags >> tags_export_to_cloud_storage
# tags_export_to_cloud_storage >> tags_download_to_local
# [train_download_to_local, test_download_to_local, tags_download_to_local] >> train_model
