import pytest
import pandas as pd
import os
from src.ingestion.extract import extract_data

def test_extract_data(tmp_path):
    # Create mock CSV
    mock_csv = tmp_path / "mock_flights.csv"
    mock_csv.write_text("airline,flight,price\nIndigo,IN-123,5000\n")
    
    df = extract_data(str(mock_csv))
    
    assert len(df) == 1
    assert list(df.columns) == ['airline', 'flight', 'price']
    assert df.iloc[0]['airline'] == 'Indigo'

def test_extract_data_not_found():
    with pytest.raises(FileNotFoundError):
        extract_data("non_existent_file.csv")
