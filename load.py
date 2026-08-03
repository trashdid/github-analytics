import datetime
import json
import os

from google.cloud import storage
from google.cloud import bigquery

storage_client = storage.Client(project=f'{os.getenv("GOOGLE_CLOUD_PROJECT")}')

bucket_name = f'{os.getenv("GOOGLE_CLOUD_BUCKET")}'

bucket = storage_client.bucket(bucket_name)

if bucket.exists():
    print(f'Status: Connected to an Existing Google Cloud Bucket: \'{bucket.name}\'.')
else:
    print(f'Status: Bucket \'{bucket_name}\' does not exist. Provisioning new bucket...')
    bucket = storage_client.create_bucket(bucket_name, location='US')
    print(f'Success: Provisioned bucket \'{bucket.name}\' in location \'US\'.')

commits_destination_path = f'raw/github/jellyfin/commits/{datetime.datetime.now().strftime('%Y/%m/%d')}/data.json'
issues_destination_path = f'raw/github/jellyfin/issues/{datetime.datetime.now().strftime('%Y/%m/%d')}/data.json'
pulls_destination_path = f'raw/github/jellyfin/pulls/{datetime.datetime.now().strftime('%Y/%m/%d')}/data.json'

# This is where the loading from local file should be changed
with open('commits_data_sample.json', 'r', encoding='utf-8') as file:
    commits_data = json.load(file)

with open('pulls_data_sample.json', 'r', encoding='utf-8') as file:
    pulls_data = json.load(file)

with open('issues_data_sample.json', 'r', encoding='utf-8') as file:
    issues_data = json.load(file)

commits_ndjson_payload = '\n'.join([json.dumps(record) for record in commits_data])

commits_blob = bucket.blob(commits_destination_path)

commits_blob.upload_from_string(data=commits_ndjson_payload, content_type='application/x-ndjson')


issues_ndjson_payload = '\n'.join([json.dumps(record) for record in issues_data])

issues_blob = bucket.blob(issues_destination_path)

issues_blob.upload_from_string(data=issues_ndjson_payload, content_type='application/x-ndjson')


pulls_ndjson_payload = '\n'.join([json.dumps(record) for record in pulls_data])

pulls_blob = bucket.blob(pulls_destination_path)

pulls_blob.upload_from_string(data=pulls_ndjson_payload, content_type='application/x-ndjson')


bigquery_client = bigquery.Client(project=f'{os.getenv("GOOGLE_CLOUD_PROJECT")}')

dataset_id = f'{os.getenv("GOOGLE_CLOUD_PROJECT")}.github_raw_data'

commits_gcs_uri = f"gs://{bucket_name}/{commits_destination_path}"
commits_table_id = f'{dataset_id}.raw_commits'

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
)

print(f'Loading {commits_gcs_uri} into BigQuery table {commits_table_id}...')
load_job = bigquery_client.load_table_from_uri(commits_gcs_uri, commits_table_id, job_config=job_config)
load_job.result()

pulls_gcs_uri = f"gs://{bucket_name}/{pulls_destination_path}"
pulls_table_id = f'{dataset_id}.raw_pulls'

print(f'Loading {pulls_gcs_uri} into BigQuery table {pulls_table_id}...')
load_job = bigquery_client.load_table_from_uri(pulls_gcs_uri, pulls_table_id, job_config=job_config)
load_job.result()

issues_gcs_uri = f"gs://{bucket_name}/{issues_destination_path}"
issues_table_id = f'{dataset_id}.raw_issues'

print(f'Loading {issues_gcs_uri} into BigQuery table {issues_table_id}...')
load_job = bigquery_client.load_table_from_uri(issues_gcs_uri, issues_table_id, job_config=job_config)
load_job.result()

print("Success: Pipeline ingestion complete.")