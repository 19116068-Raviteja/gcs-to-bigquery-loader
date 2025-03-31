import os
import csv
import json
import logging
from google.cloud import storage, bigquery

# Initialize clients
storage_client = storage.Client()
bigquery_client = bigquery.Client()

# Get environment variables
PROJECT_ID = os.environ["PROJECT_ID"]
DATASET_ID = os.environ["DATASET_ID"]
TABLE_ID = os.environ["TABLE_ID"]

def process_file(event, context):
    """Triggered when a new file is uploaded to GCS."""
    bucket_name = event['bucket']
    file_name = event['name']

    logging.info(f"Processing file: {file_name} from bucket: {bucket_name}")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download file from GCS
    content = blob.download_as_text()
    rows = parse_csv(content)

    if rows:
        load_data_to_bigquery(rows)
        logging.info(f"File {file_name} loaded successfully into BigQuery.")

def parse_csv(content):
    """Parses CSV content into a list of dictionaries."""
    try:
        rows = []
        reader = csv.DictReader(content.splitlines())
        for row in reader:
            rows.append(row)
        return rows
    except Exception as e:
        logging.error(f"Error parsing CSV: {e}")
        return []

def load_data_to_bigquery(rows):
    """Loads parsed data into BigQuery table."""
    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLE_ID)
    errors = bigquery_client.insert_rows_json(table_ref, rows)

    if errors:
        logging.error(f"BigQuery insertion errors: {errors}")
    else:
        logging.info("Data successfully inserted into BigQuery.")
