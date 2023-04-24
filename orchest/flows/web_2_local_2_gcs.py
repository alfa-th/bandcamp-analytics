from orkestra.utils import fetch_zip_data, upload_to_gcs, remove_files_in_folder
from orkestra.transform import df_to_parquets, rename_dataframe
import polars as pl
from prefect import flow
from prefect_gcp import GcpCredentials, GcsBucket
from pathlib import Path
from prefect.filesystems import LocalFileSystem


@flow(log_prints=True)
def main():
    gcp_creds = GcpCredentials.load("de-zoomcamp-capstone")
    gcs_block = GcsBucket(bucket="bandcamp", gcp_credentials=gcp_creds)
    data_folder = Path(LocalFileSystem.load("local-data").basepath)

    temp_folder = data_folder / "buffer"
    data_file = data_folder / "bandcamp-sales.csv"

    if not data_file.is_file():
        fetch_zip_data(
            url=(
                "https://www.dropbox.com/s/"
                "wd38q80el16i19q/1000000-bandcamp-sales.zip?dl=1"
            ),
            folder=data_folder,
            zip_name="1000000-bandcamp-sales.zip",
            csv_name="1000000-bandcamp-sales.csv",
            new_csv_name="bandcamp-sales.csv",
        )

    df = pl.read_csv(data_file)
    df = rename_dataframe(df)
    df_to_parquets(df, temp_folder)
    upload_to_gcs(gcs_block, temp_folder)
    remove_files_in_folder(temp_folder)
