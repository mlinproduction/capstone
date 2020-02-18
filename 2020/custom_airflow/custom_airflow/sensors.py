from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.bigquery_sensor import BigQueryTableSensor


class BigQueryWildcardTableSuffixSensor(BigQueryTableSensor):
    @apply_defaults
    def __init__(self, initial_suffix, final_suffix=None, *args, **kwargs):
        self.template_fields += ('initial_suffix', 'final_suffix',)
        super().__init__(*args, **kwargs)
        self.initial_suffix = initial_suffix
        self.final_suffix = final_suffix if final_suffix else initial_suffix

    def poke(self, context):
        table_uri = "`{0}.{1}.{2}` WHERE _TABLE_SUFFIX BETWEEN '{3}' AND '{4}'"\
            .format(self.project_id, self.dataset_id, self.table_id,
                    self.initial_suffix, self.final_suffix)
        self.log.info('Sensor checks existence of table: %s', table_uri)
        task_instance = context['task_instance']
        task_instance.xcom_push('table_uri', table_uri)
        return True


class CustomBigQueryTableSensor(BigQueryTableSensor):
    def poke(self, context):
        table_uri = '`{0}.{1}.{2}`'.format(self.project_id, self.dataset_id, self.table_id)
        task_instance = context['task_instance']
        task_instance.xcom_push('table_uri', table_uri)
        return super().poke(context)
