import pytest
import pandas as pd
from src.validation.quality_checks import run_quality_checks, DataQualityError

def test_validation_success():
    df = pd.DataFrame({
        'airline': ['Indigo'],
        'flight': ['IN-123'],
        'source_city': ['Delhi'],
        'departure_time': ['Morning'],
        'stops': ['zero'],
        'arrival_time': ['Night'],
        'destination_city': ['Mumbai'],
        'class': ['Economy'],
        'duration': [2.5],
        'days_left': [10],
        'price': [5000]
    })
    
    clean_df = run_quality_checks(df)
    assert len(clean_df) == 1

def test_validation_missing_columns():
    df = pd.DataFrame({'airline': ['Indigo'], 'price': [5000]})
    with pytest.raises(DataQualityError):
        run_quality_checks(df)

def test_numerical_bounds():
    df = pd.DataFrame({
        'airline': ['Indigo', 'SpiceJet', 'AirIndia'],
        'flight': ['IN-123', 'SG-123', 'AI-123'],
        'source_city': ['Delhi', 'Delhi', 'Delhi'],
        'departure_time': ['Morning', 'Morning', 'Morning'],
        'stops': ['zero', 'zero', 'zero'],
        'arrival_time': ['Night', 'Night', 'Night'],
        'destination_city': ['Mumbai', 'Mumbai', 'Mumbai'],
        'class': ['Economy', 'Economy', 'Economy'],
        'duration': [2.5, -1, 2.0], # -1 is invalid (drops row 1)
        'days_left': [10, 5, -5], # -5 is invalid (drops row 2)
        'price': [5000, 6000, 0] # 0 is invalid (drops row 2)
    })
    
    clean_df = run_quality_checks(df)
    assert len(clean_df) == 1 # Only the first row is completely valid
