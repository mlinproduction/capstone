from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from googleapiclient.errors import HttpError
from datetime import datetime
from datetime import timedelta


class CustomBigQueryHook(BigQueryHook):
    def _get_suffixes(self, initial_suffix, final_suffix):
        initial_date = datetime.strptime(initial_suffix, '%Y%m%d')
        final_date = datetime.strptime(final_suffix, '%Y%m%d')
        days = (final_date - initial_date).days + 1
        return [(initial_date + timedelta(d)).strftime('%Y%m%d')
                for d in range(days)]

    def table_range_exists(self, project_id, dataset_id, table_id,
                           initial_suffix, final_suffix):
        service = self.get_service()
        expected_tables =\
            [table_id.replace('*', suffix)
             for suffix in self._get_suffixes(initial_suffix, final_suffix)]
        first_expected_table = min(expected_tables)
        last_expected_table = max(expected_tables)
        found_tables = []
        next_page_token = None
        try:
            while True:
                results = service.tables().list(
                    projectId=project_id, datasetId=dataset_id, maxResults=100,
                    pageToken=next_page_token)\
                    .execute(num_retries=self.num_retries)
                next_page_token = results['nextPageToken']\
                    if 'nextPageToken' in results else None
                current_page_tables =\
                    [t['tableReference']['tableId'] for t in results['tables']]
                found_tables.extend(
                    [table_id for table_id in current_page_tables
                     if table_id >= first_expected_table
                     and table_id <= last_expected_table])

                if not(next_page_token):
                    break

            return len(set(expected_tables).difference(set(found_tables))) == 0
        except HttpError as e:
            if e.resp['status'] == '404':
                return False
            raise
