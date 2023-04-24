from google.cloud.bigquery import LoadJobConfig, SourceFormat, SchemaField
from google.cloud.bigquery.table import TimePartitioning, TimePartitioningType

from typing import List


def get_load_job_config(
    schema: List[SchemaField],
    time_partitioning: TimePartitioning,
    clustering_fields: List[str],
):
    config = LoadJobConfig(
        source_format=SourceFormat.PARQUET,
        schema=schema,
        time_partitioning=time_partitioning,
        clustering_fields=clustering_fields,
    )
    
    return config
