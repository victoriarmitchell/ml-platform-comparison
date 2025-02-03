from pathlib import Path
import pandas as pd
import subprocess
import typer
from loguru import logger

from ml_platform_comparison.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()  # Initialize Typer CLI app

def run_command(command):
    """Helper function to run shell commands safely."""
    try:
        logger.info(f"Executing command: {command}")
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(e.stderr)

def dvc_pull():
    """Ensures that the latest raw data is pulled from DVC if it's missing."""
    try:
        logger.info("Pulling latest raw data from DVC...")
        run_command("dvc pull")
        logger.success("DVC pull complete.")
    except Exception as e:
        logger.error(f"DVC pull failed: {e}")

@app.command()  # Correct way to register a Typer command
def preprocess():
    """Preprocesses all files in RAW_DATA_DIR and saves them in PROCESSED_DATA_DIR with `_processed` appended to filenames."""
    dvc_pull()
    
    if not RAW_DATA_DIR.exists():
        logger.error(f"RAW_DATA_DIR does not exist: {RAW_DATA_DIR}")
        return

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file in RAW_DATA_DIR.glob("*.csv"):
        logger.info(f"Processing {file.name}...")

        try:
            df = pd.read_csv(file)

            # Basic preprocessing
            logger.info(f"Handling missing values for {file.name}...")
            df.fillna(method='ffill', inplace=True)

            logger.info(f"Dropping duplicate rows for {file.name}...")
            df.drop_duplicates(inplace=True)

            logger.info(f"Converting categorical features for {file.name}...")
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                df[col] = df[col].astype('category')

            # Generate processed filename with "_processed"
            processed_filename = file.stem + "_processed.csv"
            processed_file = PROCESSED_DATA_DIR / processed_filename

            # Save processed data
            df.to_csv(processed_file, index=False)
            logger.success(f"Processed file saved: {processed_file}")

            # Track processed data with DVC
            run_command(f"dvc add {processed_file}")

        except Exception as e:
            logger.error(f"Error processing {file.name}: {e}")

    # Commit and push all processed files
    run_command("git add data/processed/*.dvc")
    run_command("git commit -m 'Track all processed datasets with DVC'")
    run_command("dvc push")

    logger.success("All processed datasets are tracked and pushed to DVC!")

if __name__ == "__main__":
    app()  # Ensures Typer recognizes commands