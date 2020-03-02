from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
import os


class CustomBigQueryOperator(BigQueryOperator):
    def get_custom_context(self, context):
        return context

    def render_template(self, content, context, jinja_env=None, seen_oids=None):
        context = self.get_custom_context(context)
        return super().render_template(content, context, jinja_env, seen_oids)

    def execute(self, context):
        task_instance = context['task_instance']
        task_instance.xcom_push('output_table_name', f'`{self.destination_dataset_table}`')
        super().execute(context)


class CustomBigQueryToCloudStorageOperator(BigQueryToCloudStorageOperator):
    def execute(self, context):
        task_instance = context['task_instance']
        task_instance.xcom_push('destination_cloud_storage_uris',
                                f'`{self.destination_cloud_storage_uris}`')
        super().execute(context)


class CustomGoogleCloudStorageDownloadDirectoryOperator(BaseOperator):
    template_fields = ('bucket', 'prefix', 'directory',)

    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self,
                 bucket,
                 prefix,
                 directory,
                 google_cloud_storage_conn_id='google_cloud_default',
                 delegate_to=None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.bucket = bucket
        self.prefix = prefix
        self.directory = directory
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        self.log.info('Executing download: %s, %s, %s', self.bucket,
                      self.prefix, self.bucket)
        hook = GoogleCloudStorageHook(
            google_cloud_storage_conn_id=self.google_cloud_storage_conn_id,
            delegate_to=self.delegate_to
        )

        downloaded_files = []
        for object in hook.list(bucket=self.bucket, prefix=self.prefix):
            self.log.info('Downloading object: %s', object)
            filename = os.path.join(self.directory, object.replace('/', '_'))
            hook.download(bucket=self.bucket,
                          object=object,
                          filename=filename)
            downloaded_files.append(filename)

        task_instance = context['task_instance']
        task_instance.xcom_push('downloaded_files', downloaded_files)
