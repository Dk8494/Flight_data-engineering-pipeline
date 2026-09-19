import pandas as pd
import os
from src.utils.config import logger

class DataExtractionError(Exception):
    pass

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extract data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Extracted data.
    """
    logger.info(f"Starting data extraction from {file_path}")
    
    if not os.path.exists(file_path):
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully extracted {len(df)} rows from {file_path}")
        return df
    except Exception as e:
        error_msg = f"Error reading CSV file: {str(e)}"
        logger.error(error_msg)
        raise DataExtractionError(error_msg)

if __name__ == "__main__":
    from src.utils.config import DATA_SOURCE_PATH
    try:
        df = extract_data(DATA_SOURCE_PATH)
        print(df.head())
    except Exception as e:
        print(f"Extraction failed: {e}")
