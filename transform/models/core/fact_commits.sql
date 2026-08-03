WITH commits AS (
    SELECT * FROM {{ ref('staging_github_commits') }}
),

users AS (
    SELECT * FROM {{ ref('dim_github_users') }}
)

SELECT
    c.commit_hash,
    u.author_id,
    c.commit_timestamp,
    c.commit_message,
    1 AS commit_count
FROM commits c
LEFT JOIN users u
    ON c.author_email = u.author_email