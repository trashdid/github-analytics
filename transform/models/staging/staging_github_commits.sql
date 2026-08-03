WITH commit_source_data AS (
    SELECT * FROM {{ source('github_raw', 'raw_commits') }}
),

renamed AS (
    SELECT
        sha AS commit_hash,
        commit.author.name AS author_name,
        commit.author.email AS author_email,
        committer.id AS author_id,
        committer.type AS author_type,
        CAST(commit.author.date AS TIMESTAMP) AS commit_timestamp,
        commit.message AS commit_message,
        url AS commit_url
    FROM commit_source_data
)

SELECT * FROM renamed