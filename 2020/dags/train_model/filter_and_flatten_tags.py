from custom_airflow.operators import CustomBigQueryOperator
from airflow.models import Variable


class FilterAndFlattenTags(CustomBigQueryOperator):
    def __init__(self, dag, train=True, *args, **kwargs):
        self.train = train
        task_id = ('train' if train else 'test') + '_filter_and_flatten_tags'
        sql = 'sql/filter_and_flatten_tags.sql'
        destination_dataset_table = '{0}.{1}.{2}_filtered_and_flattened_tags'\
            .format(Variable.get('gcp_project_id'),
                    Variable.get('work_bigquery_dataset_id'),
                    'train' if train else 'test')
        super().__init__(task_id=task_id, dag=dag, sql=sql,
                         destination_dataset_table=destination_dataset_table,
                         *args, **kwargs)

    def get_custom_context(self, context):
        context['input_tables'] =\
            [context['task_instance'].xcom_pull(task_ids='select_tags', key='output_table_name'),
             context['task_instance'].xcom_pull(task_ids=('train' if self.train else 'test') + '_tagged_posts_sensor', key='output_table_name')]
        return context
