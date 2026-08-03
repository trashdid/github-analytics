WITH issue_source_data AS (
    SELECT * FROM {{ source('github_raw', 'raw_issues') }}
),

renamed AS (
    SELECT
        id AS issue_id,
        number AS issue_number,
        title AS issue_title,
        state AS issue_state,
        type AS issue_type,
        pull_request.url AS pull_request_url,
        author_association,
        user.id AS author_id,
        user.type AS author_type
    FROM issue_source_data
)

SELECT * FROM renamed