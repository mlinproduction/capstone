from custom_airflow.operators import CustomBigQueryOperator
from airflow.models import Variable


class SelectTags(CustomBigQueryOperator):
    def __init__(self, dag, *args, **kwargs):
        task_id = 'select_tags'
        sql = 'sql/select_tags.sql'
        destination_dataset_table = '{0}.{1}.selected_tags'\
            .format(Variable.get('gcp_project_id'), Variable.get('work_bigquery_dataset_id'))
        super().__init__(
            task_id=task_id, dag=dag, sql=sql,
            destination_dataset_table=destination_dataset_table,
            *args, **kwargs)

    def get_custom_context(self, context):
        context['input_tables'] =\
            [context['task_instance'].xcom_pull(task_ids='train_tagged_posts_sensor', key='output_table_name'),
             context['task_instance'].xcom_pull(task_ids='tags_table_sensor', key='output_table_name')]
        context['num_labels'] = Variable.get('num_labels')
        return context
