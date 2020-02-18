{% set flattened_tags_sensor = params['train_test'] ~ '_flatten_tags' %}
{% set titles_sensor = params['train_test'] ~ '_titles_sensor' %}
WITH
  flattened_tags AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids=flattened_tags_sensor, key='table_uri') }}),
  titles AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids=titles_sensor, key='table_uri') }})
SELECT
  t1.*,
  title
FROM
  flattened_tags AS t1
JOIN
  titles AS t2
ON
  t1.post_id = t2.id
