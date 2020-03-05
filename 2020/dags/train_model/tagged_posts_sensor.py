from custom_airflow.sensors import BigQueryWildcardTableSuffixSensor
from airflow.models import Variable


class TaggedPostsSensor(BigQueryWildcardTableSuffixSensor):
    def __init__(self, dag, train=True, *args, **kwargs):
        task_id = ('train' if train else 'test') + '_tagged_posts_sensor'
        dataset_id = Variable.get('input_bigquery_dataset_id')
        table_id = 'stackoverflow_posts_tags_*'
        initial_suffix = Variable.get(
            'initial_{}_pdate'.format('train' if train else 'test'))
        final_suffix = Variable.get(
            'final_{}_pdate'.format('train' if train else 'test'))
        super().__init__(
            task_id=task_id, dag=dag, dataset_id=dataset_id, table_id=table_id,
            initial_suffix=initial_suffix, final_suffix=final_suffix,
            timeout=60, *args, **kwargs)
