from pathlib import Path
import polars as pl
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_shell import ShellOperation


@task()
def fetch_zip_data(
    url: str,
    folder: Path,
    zip_name="1000000-bandcamp-sales.zip",
    csv_name="1000000-bandcamp-sales.csv",
    new_csv_name="bandcamp-sales.csv",
):
    ShellOperation(
        commands=[
            f"wget {url} -O {zip_name}",
            f"unzip {zip_name} -d .",
            f"mv {csv_name} {new_csv_name}",
            f"rm -f {zip_name}",
        ],
        working_dir=folder,
    ).run()

    return


@task()
def fetch_bandcamp_data(folder: Path):
    fetch_zip_data.fn(
        url="https://www.dropbox.com/s/wd38q80el16i19q/1000000-bandcamp-sales.zip?dl=1",
        folder=folder,
        zip_name="1000000-bandcamp-sales.zip",
        csv_name="1000000-bandcamp-sales.csv",
        new_csv_name="bandcamp-sales.csv",
    )

@task()
def upload_to_gcs(gcs_block: GcsBucket, folderpath: Path):
    for filepath in folderpath.glob("*.parquet"):
        gcs_block.upload_from_path(filepath)

    return


@task()
def remove_files_in_folder(folder_path: Path):
    assert folder_path.is_dir()

    for file in folder_path.glob("*.parquet"):
        file.unlink()
