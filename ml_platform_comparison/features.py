import typer
from pathlib import Path
import pandas as pd
import featuretools as ft
import subprocess
from loguru import logger

from ml_platform_comparison.config import PROCESSED_DATA_DIR

app = typer.Typer()  # Initialize Typer CLI app

def run_command(command: str):
    """Helper function to run shell commands safely."""
    try:
        logger.info(f"Executing command: {command}")
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(e.stderr)

def dvc_pull():
    """Ensures that the latest processed data is pulled from DVC if it's missing."""
    try:
        logger.info("Pulling latest processed data from DVC...")
        run_command("dvc pull")
        logger.success("DVC pull complete.")
    except Exception as e:
        logger.error(f"DVC pull failed: {e}")

@app.command()
def generate_features():
    """Generates features using Featuretools with transaction and identity datasets."""
    dvc_pull()
    
    if not PROCESSED_DATA_DIR.exists():
        logger.error(f"PROCESSED_DATA_DIR does not exist: {PROCESSED_DATA_DIR}")
        return

    feature_dir = PROCESSED_DATA_DIR / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)

    dataframes = {}
    
    for file in PROCESSED_DATA_DIR.glob("*.csv"):
        logger.info(f"Loading {file.name} for feature engineering...")
        try:
            df = pd.read_csv(file)
            dataframes[file.stem] = df
            logger.success(f"Loaded {file.name} with {df.shape[0]} rows and {df.shape[1]} columns.")
        except Exception as e:
            logger.error(f"Failed to load {file.name}: {e}")

    if "train_transaction" not in dataframes:
        logger.error("train_transaction dataset is required for feature engineering.")
        return
    if "train_identity" not in dataframes:
        logger.warning("train_identity dataset not found. Proceeding with only transactions.")

    transactions_df = dataframes["train_transaction"]
    identity_df = dataframes.get("train_identity")

    # Merge identity info into transactions if available
    if identity_df is not None:
        logger.info("Merging identity features with transactions...")
        full_df = transactions_df.merge(identity_df, on="TransactionID", how="left")
    else:
        full_df = transactions_df

    # Create an EntitySet
    logger.info("Setting up Featuretools entity set...")
    es = ft.EntitySet(id="fraud_detection")

    es = es.add_dataframe(
        dataframe_name="transactions",
        dataframe=full_df,
        index="TransactionID",
        time_index="TransactionDT"
    )

    # Automated feature engineering
    logger.info("Generating new features with Featuretools...")
    feature_matrix, feature_defs = ft.dfs(
        entityset=es,
        target_dataframe_name="transactions",
        agg_primitives=["sum", "mean", "max", "min", "std", "count", "n_unique"],
        trans_primitives=["month", "day", "weekday", "is_weekend"]
    )

    logger.success(f"Generated {feature_matrix.shape[1]} features!")

    # Save feature matrix
    feature_file = feature_dir / "train_transaction_features.csv"
    feature_matrix.to_csv(feature_file, index=False)
    
    logger.success(f"Feature matrix saved to {feature_file}")

    # Track processed features with DVC
    run_command(f"dvc add {feature_file}")

    # Commit and push all feature files
    run_command("git add data/processed/features/*.dvc")
    run_command("git commit -m 'Track all generated feature datasets with DVC'")
    run_command("dvc push")

    logger.success("All feature datasets are tracked and pushed to DVC!")

if __name__ == "__main__":
    app()  # Ensures Typer recognizes commands