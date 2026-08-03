WITH commits AS (
    SELECT
        author_name,
        author_email,
        author_id,
        author_type,
        CAST(NULL AS STRING) AS author_association
    FROM {{ ref('staging_github_commits') }}
),

issues AS (
  SELECT
      CAST(NULL AS STRING) AS author_name,
      CAST(NULL AS STRING) AS author_email,
      author_id,
      author_type,
      author_association
  FROM {{ ref('staging_github_issues') }}
),

unioned_users AS (
    SELECT * FROM commits
    UNION ALL
    SELECT * FROM issues
)

SELECT
    author_id,
    COALESCE(MAX(author_name), 'Unknown') AS author_name,
    COALESCE(MAX(author_email), 'Unknown') AS author_email,
    author_type,
    COALESCE(MAX(author_association), 'Unknown') AS author_association
FROM unioned_users
GROUP BY author_id, author_type