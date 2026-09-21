import pandas as pd
import hashlib
from src.utils.config import logger

def generate_flight_key(row) -> str:
    """Generate a unique surrogate key for each flight fact record based on deterministic fields."""
    # We combine key fields to identify a unique observed flight fare record.
    # The combination of flight_id, source, destination, class, days_left, and price serves as a unique signature.
    key_string = f"{row['flight']}_{row['source_city']}_{row['destination_city']}_{row['class']}_{row['days_left']}_{row['price']}"
    return hashlib.md5(key_string.encode()).hexdigest()

def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize string columns (trim, title case)."""
    string_cols = ['airline', 'source_city', 'destination_city', 'departure_time', 'arrival_time', 'class', 'stops']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    return df

def map_stops(df: pd.DataFrame) -> pd.DataFrame:
    """Map categorical stops to numerical/standardized values."""
    if 'stops' in df.columns:
        stop_map = {
            'Zero': 0,
            'One': 1,
            'Two_Or_More': 2
        }
        df['stops_numeric'] = df['stops'].map(stop_map).fillna(-1).astype(int)
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Main transformation pipeline."""
    logger.info("Starting data transformations.")
    
    # Create copy to avoid SettingWithCopyWarning
    df_transformed = df.copy()
    
    # Normalize strings
    df_transformed = normalize_strings(df_transformed)
    
    # Map stops
    df_transformed = map_stops(df_transformed)
    
    # Generate unique ID for idempotency (UPSERT)
    df_transformed['fact_id'] = df_transformed.apply(generate_flight_key, axis=1)
    
    # Create route column for analytics
    df_transformed['route'] = df_transformed['source_city'] + '-' + df_transformed['destination_city']
    
    # Drop duplicates based on the fact_id to ensure we don't try to insert identical records
    initial_len = len(df_transformed)
    df_transformed = df_transformed.drop_duplicates(subset=['fact_id'])
    dropped = initial_len - len(df_transformed)
    if dropped > 0:
        logger.info(f"Dropped {dropped} completely duplicated records during transformation.")
        
    logger.info("Data transformations completed.")
    return df_transformed
