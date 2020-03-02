from custom_airflow.sensors import CustomBigQueryTableSensor
from airflow.models import Variable


class TagsTableSensor(CustomBigQueryTableSensor):
    def __init__(self, dag, *args, **kwargs):
        task_id = 'tags_table_sensor'
        dataset_id = Variable.get('input_bigquery_dataset_id')
        table_id = 'tags'
        super().__init__(
            task_id=task_id, dag=dag, dataset_id=dataset_id, table_id=table_id,
            timeout=60, *args, **kwargs)
