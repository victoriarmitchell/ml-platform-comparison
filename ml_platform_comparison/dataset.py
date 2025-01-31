from pathlib import Path
import pandas as pd
import subprocess
import typer
from loguru import logger
from tqdm import tqdm

from ml_platform_comparison.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

@app.command()
def dvc_pull():
    """
    Ensures that the latest data is pulled from DVC if it's missing.
    """
    try:
        logger.info("Checking if raw data exists locally...")
        if not (RAW_DATA_DIR / "train_transaction.csv").exists():
            logger.warning("Raw data not found locally. Pulling from DVC...")
            subprocess.run(["dvc", "pull", "data/raw/train_transaction.csv"], check=True)
            logger.success("DVC pull complete.")
    except subprocess.CalledProcessError:
        logger.error("DVC pull failed. Make sure you have access to the remote storage.")

@app.command()
def load_data():
    """
    Loads the dataset from the raw data directory. Calls dvc_pull() if the file is missing.
    """
    dvc_pull()  # Ensure data is available
    file_path = RAW_DATA_DIR / "train_transaction.csv"

    if file_path.exists():
        logger.info(f"Loading dataset from {file_path}")
        df = pd.read_csv(file_path)
        logger.success("Dataset loaded successfully!")
        print(df.head())  # Display first few rows
    else:
        logger.error(f"Dataset not found at {file_path}")

if __name__ == "__main__":
    app()