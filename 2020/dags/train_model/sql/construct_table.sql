WITH
  flattened_tags AS (
  SELECT
    *
  FROM
    {{ input_tables[0] }}),
  titles AS (
  SELECT
    *
  FROM
    {{ input_tables[1] }})
SELECT
  t1.*,
  title
FROM
  flattened_tags AS t1
JOIN
  titles AS t2
ON
  t1.post_id = t2.id
