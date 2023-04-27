from prefect import flow
from prefect_gcp import GcpCredentials
from orkestra.schema import BANDCAMP_SCHEMA
from orkestra.bigquery import get_load_job_config
from google.cloud.bigquery import (
    Client,
    DatasetReference,
    TimePartitioning,
    TimePartitioningType,
    LoadJob,
)

TABLE_ID = "de-zoomcamp-capstone.bandcamp.partitioned_clustered_root"
DATASET_ID = "de-zoomcamp-capstone.bandcamp"
BUCKET_NAME = "bandcamp"
GCS_URI = f"gs://{BUCKET_NAME}/*.parquet"
LOCATION = "asia-southeast1"

@flow
def main():
    gcp_creds = GcpCredentials.load("de-zoomcamp-capstone")
    assert isinstance(gcp_creds, GcpCredentials)
    client = gcp_creds.get_bigquery_client()
    assert isinstance(client, Client)

    
    client.create_dataset(DATASET_ID, exists_ok=True)

    # Partition by day because its already the way the data are split and
    # partitioning by something else but this doesnt make sense
    time_partitioning = TimePartitioning(
        type_=TimePartitioningType.DAY, field="utc_date"
    )

    # Clustering by country can help map visualization
    job_config = get_load_job_config(
        BANDCAMP_SCHEMA, time_partitioning, ["country"]
    )

    load_job = client.load_table_from_uri(
        source_uris=[GCS_URI],
        destination=TABLE_ID,
        location=LOCATION,
        job_config=job_config,
    )
    assert isinstance(load_job, LoadJob)

    load_job.result()
