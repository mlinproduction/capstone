from airflow import DAG
from airflow.models import Variable
import datetime


from .titles_sensor import TitlesSensor
from .tagged_posts_sensor import TaggedPostsSensor
from .tags_table_sensor import TagsTableSensor
from .select_tags import SelectTags
from .filter_and_flatten_tags import FilterAndFlattenTags
from .construct_table import ConstructTable
from .export_to_cloud_storage import (ExportToCloudStorage,
                                      ExportTagsToCloudStorage)
from .download_to_local import (DownloadToLocal, TagsDownloadToLocal)
from .train_model import TrainModel


default_args = {
    'start_date': datetime.datetime.strptime('2020-02-01', '%Y-%m-%d'),
    'project_id': Variable.get('gcp_project_id'),
    'bigquery_conn_id': Variable.get('bigquery_conn_id'),
    'write_disposition': 'WRITE_TRUNCATE',
    'allow_large_results': True,
    'use_legacy_sql': False,
    'google_cloud_storage_conn_id': Variable.get('google_cloud_storage_conn_id')
}


dag = DAG(
    'train_model',
    default_args=default_args,
    description='Train model pipeline',
    schedule_interval=None)


train_titles_sensor = TitlesSensor(dag, train=True)
test_titles_sensor = TitlesSensor(dag, train=False)

train_tagged_posts_sensor = TaggedPostsSensor(dag, train=True)
test_tagged_posts_sensor = TaggedPostsSensor(dag, train=False)

tags_table_sensor = TagsTableSensor(dag)

select_tags = SelectTags(dag)
[train_tagged_posts_sensor, tags_table_sensor] >> select_tags

train_filter_and_flatten_tags = FilterAndFlattenTags(dag, train=True)
[select_tags, train_tagged_posts_sensor] >> train_filter_and_flatten_tags

test_filter_and_flatten_tags = FilterAndFlattenTags(dag, train=False)
[select_tags, test_tagged_posts_sensor] >> test_filter_and_flatten_tags

train_construct_table = ConstructTable(dag, train=True)
[train_filter_and_flatten_tags, train_titles_sensor] >> train_construct_table

test_construct_table = ConstructTable(dag, train=False)
[test_filter_and_flatten_tags, test_titles_sensor] >> test_construct_table

train_export_to_cloud_storage = ExportToCloudStorage(dag, train=True)
train_construct_table >> train_export_to_cloud_storage

test_export_to_cloud_storage = ExportToCloudStorage(dag, train=False)
test_construct_table >> test_export_to_cloud_storage

tags_export_to_cloud_storage = ExportTagsToCloudStorage(dag)
select_tags >> tags_export_to_cloud_storage

train_download_to_local = DownloadToLocal(dag, train=True)
train_export_to_cloud_storage >> train_download_to_local

test_download_to_local = DownloadToLocal(dag, train=False)
test_export_to_cloud_storage >> test_download_to_local

tags_download_to_local = TagsDownloadToLocal(dag)
tags_export_to_cloud_storage >> tags_download_to_local

train_model = TrainModel(dag)
[train_download_to_local, test_download_to_local, tags_download_to_local] >> train_model
