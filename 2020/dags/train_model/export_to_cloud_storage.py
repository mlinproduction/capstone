from custom_airflow.operators import CustomBigQueryToCloudStorageOperator
from airflow.models import Variable
import os


class ExportToCloudStorage(CustomBigQueryToCloudStorageOperator):
    def __init__(self, dag, train=True, *args, **kwargs):
        task_id = ('train' if train else 'test') + '_export_to_cloud_storage'
        source_project_dataset_table = \
            """{{{{ task_instance.xcom_pull(task_ids='{0}_construct_table',
                                          key='output_table_name')
                  | replace('`', '') }}}}""".format('train' if train else 'test')
        destination_cloud_storage_uris =\
            ['gs://' + os.path.join(Variable.get('gcs_bucket'),
                                    Variable.get('gcs_prefix'),
                                    '{}-table'.format('train' if train else 'test'),
                                    '*')]

        super().__init__(
            task_id=task_id, dag=dag,
            source_project_dataset_table=source_project_dataset_table,
            destination_cloud_storage_uris=destination_cloud_storage_uris,
            compression='NONE', export_format='CSV')


class ExportTagsToCloudStorage(CustomBigQueryToCloudStorageOperator):
    def __init__(self, dag, *args, **kwargs):
        task_id = 'tags_export_to_cloud_storage'
        source_project_dataset_table = \
            """{{ task_instance.xcom_pull(task_ids='select_tags', key='output_table_name')
                  | replace('`', '') }}"""
        destination_cloud_storage_uris =\
            ['gs://' + os.path.join(Variable.get('gcs_bucket'),
                                    Variable.get('gcs_prefix'),
                                    'tags', '*')]

        super().__init__(
            task_id=task_id, dag=dag,
            source_project_dataset_table=source_project_dataset_table,
            destination_cloud_storage_uris=destination_cloud_storage_uris,
            compression='NONE', export_format='CSV')
