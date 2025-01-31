from pathlib import Path
import pandas as pd
import subprocess
import typer
from loguru import logger
from tqdm import tqdm

from ml_platform_comparison.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

# initialize typer
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

@app.command()
def preprocess():
    """
    Preprocesses the dataset, saves the cleaned version, and tracks it with DVC.
    """
    dvc_pull()
    file_path = RAW_DATA_DIR / "train_transaction.csv"
    
    if not file_path.exists():
        logger.error("Raw data not found. Run 'python dataset.py load-data' first.")
        return

    logger.info(f"Loading dataset from {file_path}")
    df = pd.read_csv(file_path)

    # Basic preprocessing
    logger.info("Starting data preprocessing...")
    
    logger.info("Handling missing values...")
    df.fillna(method='ffill', inplace=True)  # Forward fill missing values

    logger.info("Dropping duplicate rows...")
    df.drop_duplicates(inplace=True)

    logger.info("Converting categorical features...")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].astype('category')

    # Save processed data
    processed_path = PROCESSED_DATA_DIR / "train_transaction_processed.csv"
    df.to_csv(processed_path, index=False)
    
    logger.success(f"Preprocessing complete! Processed data saved to {processed_path}")

    # Track processed data with DVC
    logger.info("Tracking processed data with DVC...")
    #subprocess.run(f"dvc add {processed_path}")
    subprocess.run(["dvc", "add", f"{processed_path}"], check=True)

    # Git commit
    logger.info("Committing DVC changes to Git...")
    subprocess.run(["git", "add", "."], check=True)
    #subprocess.run(["git", "add", f"{processed_path}.dvc"], check=True)
    subprocess.run(["git", "commit", "-m", "Add processed data to DVC"], check=True)

    # Push to DVC remote
    logger.info("Pushing processed data to DVC remote...")
    subprocess.run(["dvc", "push", f"{processed_path}.dvc"], check=True)

    logger.success("Processed data successfully added to DVC and pushed to remote!")

if __name__ == "__main__":
    app()