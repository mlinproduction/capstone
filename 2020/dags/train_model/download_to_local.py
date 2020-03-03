from custom_airflow.operators import CustomGoogleCloudStorageDownloadDirectoryOperator
from airflow.models import Variable


class DownloadToLocal(CustomGoogleCloudStorageDownloadDirectoryOperator):
    def __init__(self, dag, train=True, *args, **kwargs):
        task_id = ('train' if train else 'test') + '_download_to_local'
        bucket = Variable.get('gcs_bucket')
        prefix =\
            """{{{{ task_instance.xcom_pull(
                        task_ids='{0}_export_to_cloud_storage',
                        key='destination_cloud_storage_uris')
                    | replace('gs://', '')
                    | replace(var.value.gcs_bucket ~ '/', '')
                    | replace('*', '') | replace("'", '') | replace('[', '')
                    | replace(']', '') }}}}""".format('train' if train else 'test')
        directory = Variable.get('local_directory')
        super().__init__(
            task_id=task_id, dag=dag, bucket=bucket, prefix=prefix,
            directory=directory, *args, **kwargs)


class TagsDownloadToLocal(CustomGoogleCloudStorageDownloadDirectoryOperator):
    def __init__(self, dag, *args, **kwargs):
        task_id = 'tags_download_to_local'
        bucket = Variable.get('gcs_bucket')
        prefix =\
            """{{ task_instance.xcom_pull(
                        task_ids='tags_export_to_cloud_storage',
                        key='destination_cloud_storage_uris')
                    | replace('gs://', '')
                    | replace(var.value.gcs_bucket ~ '/', '')
                    | replace('*', '') | replace("'", '') | replace('[', '')
                    | replace(']', '') }}"""
        directory = Variable.get('local_directory')
        super().__init__(
            task_id=task_id, dag=dag, bucket=bucket, prefix=prefix,
            directory=directory, *args, **kwargs)
