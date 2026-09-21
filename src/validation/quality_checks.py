import pandas as pd
from src.utils.config import logger

class DataQualityError(Exception):
    pass

def validate_schema(df: pd.DataFrame, expected_columns: list) -> bool:
    """Validate that all expected columns exist in the dataframe."""
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        error_msg = f"Schema validation failed. Missing columns: {missing_cols}"
        logger.error(error_msg)
        raise DataQualityError(error_msg)
    logger.info("Schema validation passed.")
    return True

def check_missing_values(df: pd.DataFrame, critical_columns: list) -> pd.DataFrame:
    """Remove rows with missing values in critical columns and log warnings for others."""
    initial_len = len(df)
    df_clean = df.dropna(subset=critical_columns).copy()
    dropped = initial_len - len(df_clean)
    
    if dropped > 0:
        logger.warning(f"Dropped {dropped} rows due to missing values in {critical_columns}")
        
    return df_clean

def check_numerical_bounds(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure logical bounds for numerical columns."""
    initial_len = len(df)
    
    # Prices should be strictly positive
    if 'price' in df.columns:
        df = df[df['price'] > 0]
        
    # Duration should be strictly positive
    if 'duration' in df.columns:
        df = df[df['duration'] > 0]
        
    # Days left should be non-negative
    if 'days_left' in df.columns:
        df = df[df['days_left'] >= 0]
        
    dropped = initial_len - len(df)
    if dropped > 0:
        logger.warning(f"Dropped {dropped} rows due to numerical bound violations.")
        
    return df

def run_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    """Run all validation checks sequentially."""
    logger.info("Starting data quality checks.")
    
    expected_cols = [
        'airline', 'flight', 'source_city', 'departure_time', 
        'stops', 'arrival_time', 'destination_city', 'class', 
        'duration', 'days_left', 'price'
    ]
    
    validate_schema(df, expected_cols)
    df = check_missing_values(df, expected_cols)
    df = check_numerical_bounds(df)
    
    logger.info("Data quality checks completed successfully.")
    return df
