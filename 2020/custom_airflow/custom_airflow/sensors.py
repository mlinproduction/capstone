from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.bigquery_sensor import BigQueryTableSensor
from .hooks import CustomBigQueryHook


class BigQueryWildcardTableSuffixSensor(BigQueryTableSensor):
    @apply_defaults
    def __init__(self, initial_suffix, final_suffix=None, *args, **kwargs):
        self.template_fields += ('initial_suffix', 'final_suffix',)
        super().__init__(*args, **kwargs)
        self.initial_suffix = initial_suffix
        self.final_suffix = final_suffix if final_suffix else initial_suffix

    def poke(self, context):
        table_uri = '{0}.{1}.{2}'.format(self.project_id, self.dataset_id,
                                         self.table_id)
        self.log.info('Sensor checks existence of table: {} between {} and {}'
                      .format(table_uri, self.initial_suffix,
                              self.final_suffix))

        output_table_name = "`{0}` WHERE _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'"\
            .format(table_uri, self.initial_suffix, self.final_suffix)
        task_instance = context['task_instance']
        task_instance.xcom_push('output_table_name', output_table_name)

        hook = CustomBigQueryHook(
            bigquery_conn_id=self.bigquery_conn_id,
            delegate_to=self.delegate_to)
        return hook.table_range_exists(
            self.project_id, self.dataset_id, self.table_id,
            self.initial_suffix, self.final_suffix)


class CustomBigQueryTableSensor(BigQueryTableSensor):
    def poke(self, context):
        table_uri = '{0}.{1}.{2}'.format(self.project_id, self.dataset_id,
                                         self.table_id)

        output_table_name = '`{0}`'.format(table_uri)
        task_instance = context['task_instance']
        task_instance.xcom_push('output_table_name', output_table_name)
        return super().poke(context)
