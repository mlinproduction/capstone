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
    tag)
SELECT
  t1.id AS tag_id,
  t1.tag_name,
  n
FROM
  tags AS t1
JOIN
  tag_count AS t2
ON
  t1.tag_name = t2.tag
ORDER BY
  n DESC
LIMIT
  50
