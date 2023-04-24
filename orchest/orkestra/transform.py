from pathlib import Path
import polars as pl
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_shell import ShellOperation


@task
def rename_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    return df.rename({"": "row_id"})


@task
def df_to_parquets(df: pl.DataFrame, bufferpath: Path):
    grouped_df = df.with_columns(utc_date=pl.from_epoch("utc_date")).groupby(
        pl.col("utc_date").dt.date()
    )

    for group_key, group_df in grouped_df:
        filepath = bufferpath / f"bandcamp-sales_{group_key}.parquet"
        group_df.write_parquet(filepath)

    return
