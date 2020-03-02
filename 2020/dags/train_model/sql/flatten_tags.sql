{% set tagged_posts_sensor = params['train_test'] ~ '_tagged_posts_sensor' %}
WITH
  selected_tags AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids='select_tags', key='table_uri') }}),
  tagged_posts AS (
  SELECT
    *
  FROM
    {{ task_instance.xcom_pull(task_ids=tagged_posts_sensor, key='table_uri') }}),
  flattened_and_filtered_tags AS (
  SELECT
    t1.id AS post_id,
    IFNULL(t2.tag_name,
      '(other)') AS tag_name,
    t2.tag_id,
    tag_position
  FROM
    tagged_posts AS t1
  JOIN
    UNNEST(SPLIT(tags, '|')) AS tag_name
  WITH
  OFFSET
    AS tag_position
  LEFT JOIN
    selected_tags AS t2
  ON
    tag_name = t2.tag_name),
  distinct_tags AS (
  SELECT
    post_id,
    tag_name,
    MIN(tag_position) AS tag_position,
    tag_id
  FROM
    flattened_and_filtered_tags
  GROUP BY
    post_id,
    tag_name,
    tag_id)
SELECT
  * EXCEPT(tag_position),
  ROW_NUMBER() OVER(PARTITION BY post_id ORDER BY tag_position) AS tag_position
FROM
  distinct_tags
