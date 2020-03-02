WITH
  train_tags AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids='train_tagged_posts_sensor', key='table_uri') }}),
  tags AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids='tags_table_sensor', key='table_uri') }}),
  flattened_tags AS (
  SELECT
    tag
  FROM
    train_tags
  JOIN
    UNNEST(SPLIT(tags, '|')) AS tag),
  tag_count AS (
  SELECT
    tag,
    COUNT(*) AS n
  FROM
    flattened_tags
  GROUP BY
    tag),
  ordered_tag_count AS (
  SELECT
    *,
    ROW_NUMBER() OVER(ORDER BY n DESC) AS tag_order
  FROM
    tag_count)
SELECT
  DISTINCT IF(tag_order <= {{ dag_run.conf['train_params']['num_labels'] }}, t1.id, NULL) AS tag_id,
  IF(tag_order <= {{ dag_run.conf['train_params']['num_labels'] }}, t1.tag_name, '(other)') AS tag_name,
  IF(tag_order <= {{ dag_run.conf['train_params']['num_labels'] }}, t2.n, NULL) AS n
FROM
  tags AS t1
JOIN
  ordered_tag_count AS t2
ON
  t1.tag_name = t2.tag
